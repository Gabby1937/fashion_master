
from itertools import product
import json
from msilib.schema import Binary
from this import d
from unicodedata import category
#from cs50 import SQL
from flask import Flask, render_template, redirect, request, session, jsonify, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import *
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from forms import *
import random
from flask_migrate import Migrate
from flask_moment import Moment
#from jinja2.utils import markupsafe
import hashlib
import psycopg2
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, sessionmaker
#from settings import db_name, db_user, db_password
import pyrebase
from flask import g
import flask_login
import json
from flask_login import login_required, current_user, LoginManager, login_user
from models import User, Category, Product, Message, Brand, Cart, Comment, load_user
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
#gj193752

config = {
    "apiKey": "AIzaSyD1_I0gaWQGSadVRXdELf8GeTiRfeEEVqU",
    "authDomain": "fashion-master-8d4f9.firebaseapp.com",
    "projectId": "fashion-master-8d4f9",
    "storageBucket": "fashion-master-8d4f9.appspot.com",
    "messagingSenderId": "703682842868",
    "appId": "1:703682842868:web:5cb5120f72cc1c24904ea1",
    "measurementId": "G-2GKPCJB0J9",
    "databaseURL": "postgresql://master:ekka@localhost:5432/ekkadb"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


UPLOAD_FOLDER = 'static/Uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
# # Instantiate Flask object named app
app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://master:ekka@localhost:5432/ekkadb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

###################################
##### * Handling Images ###########
###################################

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/img')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app) 

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'thisismykey'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.init_app(app)
#db = firebase.database()


# database_path = 'postgresql://master:ekka@localhost:5432/ekkadb'
# engine = create_engine(database_path)
# Session = sessionmaker(engine)

connection = psycopg2.connect('postgresql://master:ekka@localhost:5432/ekkadb')
conn = connection.cursor()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.request_loader
def load_user_from_request(request):
    token = request.headers.get('Authorization')
    if token:
        user = User.verify_auth_token(token)
        if user:
            return user
    return None

#db.cursor.fetchall()

    #Home page
@app.route("/")
def index():  
    # user_id = session['user_id']
    # num = conn.execute('SELECT SUM(total) FROM carts where user_id = {};'.format(user_id[0]))
    # num = conn.fetchall()
    # shopTotal = [dict(total=row[0]) for row in num]
    # num = conn.execute("SELECT COUNT(total) FROM carts where user_id = {};".format(user_id[0]))
    # num = conn.fetchall()
    # count = [dict(total=row[0]) for row in num]
    #return render_template('index.html', count=count, sumTotal=shopTotal)
    return render_template('index.html')


#Fetch user details if logged in
def getLoginDetails():
    with conn:
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            noOfItems = 0
        else:
            loggedIn = True
            conn.execute("SELECT userId, firstName FROM users WHERE email = '" + session['email'] + "';")
            userId, firstName = conn.fetchone()
            conn.execute("SELECT count(productId) FROM kart WHERE userId = " + str(userId) + ";")
            noOfItems = conn.fetchone()[0]
    conn.close()
    return (loggedIn, firstName, noOfItems)



@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
    #Parse form data
        firstname = request.form.get('firstName')
        lastname = request.form.get('lastName')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')
        email = request.form.get('email')
        address = request.form.get('address')
        postalcode = request.form.get('postalcode')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')
        phonenumber = request.form.get('phonenumber')
        if password != confirmPassword:
            flash("Password mismatch, try again!")
        elif len(firstname) < 1 or len(lastname) < 1 or len(password) < 1 or len(email) < 1:
            flash("Please fill all required fields!")
        elif email in session:
            flash("You already have an account! Please login!")
        else:
            # Creates the user 
            auth.create_user_with_email_and_password(email, password)
            # Log the user instantly
            user = auth.sign_in_with_email_and_password(email, password)
            # In the session
            user_id = user['idToken']
            user_email = email
            session['user'] = user_id
            session['email'] = user_email
            new_user=User(firstname=firstname, lastname=lastname, address=address, postalcode=postalcode, city=city, state=state, country=country, phonenumber=phonenumber, email=email, password=hashlib.md5(password.encode()).hexdigest())
            db.session.add(new_user)
            db.session.commit()
            db.session.close()
            flash('Created successfully!')
            return redirect(url_for('login')) #redirect(url_for('login'))
    return render_template('signup.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('index'))
    
    elif request.method == 'POST':
        email = request.form.get('email')
        password  = request.form.get('password')
        #password = hashlib.md5(pword.encode()).hexdigest()
        if len(email) == 0 or len(password) == 0:
            flash('Text-field is required')
        
        try:
            # Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            # Set the session
            user_id = user['idToken']
            user_email = email
            session['user'] = user_id
            # if current_user.is_authenticated():
            #     session['userid'] = current_user.get_id()
            userid = conn.execute("select userid from users where email = '{}'".format(user_email))
            userid = conn.fetchone()
            @login_manager.user_loader
            def load_user(userid):
                userid = conn.execute("select userid from users where email = '{}'".format(user_email))
                userid = conn.fetchone()
                return User.query.get(userid)
            session['user_id']  = userid
            session['email'] = user_email
            return redirect(url_for('index'))
        except:
            flash("Invalid login!")
            return redirect(url_for('login'))
        
    return render_template("loginreal.html")


@app.route("/registerationForm")
def registrationForm():
    return redirect(url_for("signup"))


PRODUCTS_PER_PAGE = 10
def paginate_products(request, selections):
  page = request.args.get('page', 1, type=int)
  start = (page-1) * PRODUCTS_PER_PAGE
  end = start + PRODUCTS_PER_PAGE 
  
  products = [product.format() for product in selections]
  current_products = products[start:end]

  return current_products

# if current_user.is_authenticated():
#         g.user = current_user.get_id()
# def function_a(user_id):
#     os.mkdir(os.path.join(path,user_id))
#     return 'Path created successfully'


@app.route("/shop")
@login_required
def shop():
    user = current_user
    user_id = user.User.userid
    
    #page = request.args.get('page', 1, type=int)
    cur = conn.execute('SELECT name, price, percent, image_link1, image_link2, image_link3, image_link4, image_link5, description, specification, reviews, ratings, category_id, brand_id, qty, tags, video_link, colors, size, id FROM product order by id desc;')
    cur = conn.fetchall()
    products = [dict(name=row[0], price=row[1], percent=row[2], image_link1=row[3], image_link2=row[4], image_link3=row[5], image_link4=row[6], image_link5=row[7], description=row[8], specification=row[9], reviews=row[10], ratings=row[11], category_id=row[12], brand_id=row[13], qty=row[14], tags=row[15], video_link=row[16], colors=row[17], size=row[18], id=row[19]) for row in cur]
    brands = conn.execute('SELECT * FROM brand;')
    brands = conn.fetchall()
    
    max = conn.execute('SELECT category.name, category.id, count(product.category_id) as num FROM category JOIN product ON category.id = product.category_id GROUP by category.name, category.id;')
    max = conn.fetchall()
    categories = [dict(name=row[0], id=row[1], num=row[2]) for row in max]
    
    # min = conn.execute('SELECT id, count(id) as num FROM category;')
    # min = conn.fetchall()
    # count = [dict(id=row[0], num=row[1]) for row in min]
    
    cur = conn.execute('SELECT name, id FROM brand order by id desc;')
    cur = conn.fetchall()
    brand = [dict(name=row[0], id=row[1]) for row in cur]
    
    
    num = conn.execute('SELECT SUM(total) FROM carts where user_id = {};'.format(user_id[0]))
    num = conn.fetchall()
    shopTotal = [dict(total=row[0]) for row in num]
    num = conn.execute("SELECT COUNT(total) FROM carts where user_id = {};".format(user_id[0]))
    num = conn.fetchall()
    count = [dict(total=row[0]) for row in num]
    
    word = request.form.get('searchTerm')
    st = conn.execute("SELECT * from product where name like '%{}%';".format(word))
    st = conn.fetchall()
    searchTerm = [dict(name=row[0], price=row[1], percent=row[2], image_link1=row[3], image_link2=row[4], image_link3=row[5], image_link4=row[6], image_link5=row[7], description=row[8], specification=row[9], reviews=row[10], ratings=row[11], category_id=row[12], brand_id=row[13], qty=row[14], tags=row[15], video_link=row[16], colors=row[17], size=row[18], id=row[19]) for row in st]

    conn.close()

    return render_template('shops.html', title="Store Home", searchTerm=searchTerm, category=categories, products=products, brands=brand, count=count, sumTotal=shopTotal)
    
    
    
    
@app.route("/shop/search", methods=['GET', 'POST'])
def shop_search():
    if request.method == "POST":
        num = conn.execute('SELECT SUM(total) FROM carts;')
        num = conn.fetchall()
        shopTotal = [dict(total=row[0]) for row in num]
        num = conn.execute("SELECT COUNT(total) FROM carts;")
        num = conn.fetchall()
        count = [dict(total=row[0]) for row in num]
        searchTerm = request.form.get('searchTerm').lower()
        st = conn.execute("SELECT * from product where LOWER(name) like '%{}%';".format(searchTerm))
        st = conn.fetchall()
        searchTerm = [dict(id=row[0], name=row[1], price=row[2], percent=row[3], image_link1=row[4], image_link2=row[5], image_link3=row[6], image_link4=row[7], image_link5=row[8], description=row[9], specification=row[10], reviews=row[11], ratings=row[12], category_id=row[13], brand_id=row[14], qty=row[15], tags=row[16], video_link=row[17], colors=row[18], size=row[19]) for row in st]
        
        max = conn.execute('SELECT category.name, category.id, count(product.category_id) as num FROM category JOIN product ON category.id = product.category_id GROUP by category.name, category.id;')
        max = conn.fetchall()
        categories = [dict(name=row[0], id=row[1], num=row[2]) for row in max]
        
        cur = conn.execute("SELECT name, id FROM brand where LOWER(name) like '%{}%' order by id desc;")
        cur = conn.fetchall()
        brand = [dict(name=row[0], id=row[1]) for row in cur]
    
    return render_template('shops.html', title="Store Home", category=categories, products=searchTerm, brands=brand, count=count, sumTotal=shopTotal)

    

def get_all_brands():
    brands = Brand.query.join(Product, (Brand.id==Product.brand_id)).all()
    return brands

def get_all_categories():
    return Category.query.join(Product, (Category.id==Product.category_id)).all()
def discount(price, percent):
    x = price * percent / 100
    ans = price - x
    return ans
@app.route("/shop-details/<int:id>")
def shop_details(id):
    cur = conn.execute('SELECT name, id FROM brand order by id desc;')
    cur = conn.fetchall()
    brand = [dict(name=row[0], id=row[1]) for row in cur]
    max = conn.execute('SELECT category.name, category.id, count(product.category_id) as num FROM category JOIN product ON category.id = product.category_id GROUP by category.name, category.id;')
    max = conn.fetchall()
    categories = [dict(name=row[0], id=row[1], num=row[2]) for row in max]
    prod = conn.execute('SELECT name, price, percent, image_link1, image_link2, image_link3, image_link4, image_link5, description, specification, reviews, ratings, category_id, brand_id, qty, tags, video_link, colors, size FROM product WHERE id=' + str(id) + ';')
    prod = conn.fetchall()
    post = conn.execute('SELECT price FROM product where id = {};'.format(str(id)))
    post = conn.fetchall()
    pric = [dict(price=row[0]) for row in post]
    
    get = conn.execute('SELECT price, percent FROM product where id = {};'.format(str(id)))
    get = conn.fetchall()
    percen = [dict(percent=row[0]) for row in get]
    products = [dict(name=row[0], price=row[1], percent=row[2], dic=discount(row[1], row[2]), image_link1=row[3], image_link2=row[4], image_link3=row[5], image_link4=row[6], image_link5=row[7], description=row[8], specification=row[9], reviews=row[10], ratings=row[11], category_id=row[12], brand_id=row[13], qty=row[14], tags=row[15], video_link=row[16], colors=row[17], size=row[18], id=int(id)) for row in prod]
    
    return render_template('shop-details2.html', Type=type(id), productx=products, brands=brand, categories=categories) #categories=categories)

    

@app.route('/addproduct', methods=['GET','POST'])
def addproduct():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        percent = request.form.get('percent')
        image1 = request.form.get('image1')
        image2 = request.form.get('image2')
        image3 = request.form.get('image3')
        image4 = request.form.get('image4')
        image5 = request.form.get('image5')
        description = request.form.get('description')
        specification = request.form.get('specification')
        ratings = request.form.get('ratings')
        reviews = request.form.get('reviews')
        category_id = request.form.get('category_id')
        brand_id = request.form.get('brand_id')
        qty = request.form.get('qty')
        tags = request.form.get('tags')
        #carts = request.form.get('carts')
        video_link = request.form.get('video_link')
        colors = request.form.get('colors')
        size = request.form.get('size')
        
        product = Product(name=name, price=price, percent=percent,
                          image_link1=image1, image_link2=image2,
                          image_link3=image3, image_link4=image4,
                          image_link5=image5, description=description,
                          specification=specification, ratings=ratings,
                          reviews=reviews, category_id=category_id,
                          brand_id=brand_id, qty=qty, tags=tags,
                          video_link=video_link, colors=colors, size=size)
        db.session.add(product)
        db.session.commit()
        db.session.close()
        flash(name + ' was added successfully!')
        return render_template('addproduct.html')
    return render_template('addproduct.html')


def discount_price(price, percent):
    result = (price * percent) / 100
    x = price - result
    return x

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get("email")
        content = request.form.get("content")
        
        new_message=Message(name=name, email=email, content=content)
        db.session.add(new_message)
        db.session.commit()
        db.session.close()
        flash('Created successfully!')
    return render_template('contact.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/blog")
def blog():
    return render_template('blog.html')

@app.route("/blog-details", methods=['GET', 'POST'])
def blog_details():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        
        new_message=Comment(name=name, email=email, phone=phone, message=message)
        db.session.add(new_message)
        db.session.commit()
        db.session.close()
        flash('Comment successfully posted!')
    return render_template('blog-details.html')


            
            
#Add item to database
@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    if request.method == "POST":
        name = request.form['name']
        price = float(request.form['price'])
        image = request.form['image']
        description = request.form['description'] 
        specification = request.form['specification']
        reviews = request.form['reviews']
        category = request.form['category']
        brand = request.form['brand']
        stock = int(request.form['stock'])
        categoryId = int(request.form['category'])

        #Upload image
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        imagename = filename
        with conn:
            try:
                conn.execute('''INSERT INTO products (name, price, image, description, specification, reviews, category, brand, stock, categoryId) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (name, price, imagename, description, specification, reviews, category, brand, stock, categoryId))
                conn.commit()
                flash("Added successfully", category='success')
            except:
                flash("Error occurred", category='error')
                conn.rollback()
        conn.close()
        return redirect(url_for('index'))

           

            
    #Remove item from database
@app.route("/removeItem/<int:id>", methods=['GET', 'DELETE'])
def removeItem():
    productId = request.args.get('productId')
    with conn:
        try:
            conn.execute('DELETE FROM products WHERE productID = ' + productId)
            conn.commit()
            flash("Deleted successfully", category='success')
        except:
            conn.rollback()
            flash("Error occurred", category='error')
    conn.close()
    return redirect(url_for('index'))


def merge_dict(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False
    
    
@app.route("/cart")
def cart():
    user_id = session['user_id']
    ct = conn.execute('SELECT * FROM carts where user_id = {};'.format(user_id[0]))
    ct = conn.fetchall()
    cartitems = [dict(id=row[0], name=row[1], price=row[2],
                      qty=row[3], size=row[4],
                      color=row[5], image1=row[6], 
                      total=row[8], user_id=row[9]) for row in ct]
    subtotal = conn.execute('SELECT SUM(total) FROM carts where user_id = {};'.format(user_id[0]))
    subtotal = conn.fetchone()
    return render_template('shopping-cart.html', cartitems=cartitems, subtotal=subtotal)

# Add items to cart
# @app.route("/addToCart", methods=['POST'])
# def add_cart():
#     if request.method == "POST":
#         if 'userid' in session:
#             quantity = request.form.get('quantity')
#             name = request.form.get('name')
#             size = request.form.get('size')
#             color = request.form.get('colors')
#             price = request.form.get('price')
#             image = request.form.get('image')
#             id = request.form.get('id')
#             user_id=request.form.get('user_id')
#             new_item = Cart(name=name, price=price, image_link1=image, 
#                             qty=quantity, colors=color, size=size,
#                             product_id=id, total=float(price)*int(quantity), user_id=user_id)
#             db.session.add(new_item)
#             db.session.commit()
#             db.session.close()
#             flash('{} Was successfully added to carts'.format(name))
#             return redirect(url_for('shop'))
#         else:
#             return redirect(url_for('login'))
            

# Add items to cart
@app.route("/addToCart", methods=['POST'])
def add_cart():
    if request.method == "POST":
        quantity = request.form.get('quantity')
        name = request.form.get('name')
        size = request.form.get('size')
        color = request.form.get('colors')
        price = request.form.get('price')
        image = request.form.get('image')
        id = request.form.get('id')
        user_id = session['user_id']
        #user_id=request.form.get('user_id')
        new_item = Cart(name=name, price=price, image_link1=image, 
                        qty=quantity, colors=color, size=size,
                        product_id=id, total=float(price)*int(quantity), user_id=user_id)
        db.session.add(new_item)
        db.session.commit()
        db.session.close()
        flash("{} Successfully added to cart!".format(name))
        return redirect(url_for('shop'))

  
@app.route('/deletefromcart/<int:id>', methods=['GET', 'DELETE'])
def delete_cart(id):
    cname = request.form.get('name')
    conn.execute('DELETE FROM carts WHERE id = {};'.format(id))
    flash('Item with ID {} successfully removed from Cart;'.format(id))
    return redirect(url_for('cart'))
# @app.route('/cart')
# def get_cart():
#     if 'shopcart' not in session:
#         return redirect(request.referrer)
#     total_without_tax = 0
#     for key, product in session['shopcart'].items():
#         # subtotal = 0
#         # subtotal += product['price']*product['quantity']
#         # # tax += round(0.06 * subtotal, 0)
#         total_without_tax += product['price']*int(product['quantity'])
#         # total += round((subtotal + tax), 2)  
#     return render_template('carts.html', title="Your Cart", total_without_tax=total_without_tax, brands=get_all_brands(),
#                             categories=get_all_categories())
    
# @app.route('/cart')
# def get_cart():
#     if 'shopcart' not in session:
#         return redirect(request.referrer)
#     total_without_tax = 0
#     for key, product in session['shopcart'].items():
#         # subtotal = 0
#         # subtotal += product['price']*product['quantity']
#         # # tax += round(0.06 * subtotal, 0)
#         total_without_tax += product['price']*int(product['quantity'])
#         # total += round((subtotal + tax), 2)  
#     return render_template('carts.html', title="Your Cart", total_without_tax=total_without_tax, brands=get_all_brands(),
#                             categories=get_all_categories())
    
    
@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('shop'))
    except Exception as e:
        print(e)
        
        
@app.route('/updatecart', methods=["POST"])
def updatecart():
    id = request.form.get('cartid')
    qty = request.form.get('qty')
    price = request.form.get('price')
    # st = conn.execute('SELECT SUM(total) FROM cart;')
    # st = conn.fetchall()
    # subtotal = [dict(subtotal = row[0]) for row in st]
    conn.execute('UPDATE carts SET qty={} where id = {};'.format(qty, id))
    return redirect(url_for('cart'))
        
# @app.route('/updatecart/<int:code>', methods=["POST"])
# def updatecart(code):
#     if 'shopcart' not in session and len(session['shopcart']) <= 0:
#         return redirect(url_for('shop'))
#     if request.method == "POST":
#         quantity = request.form.get('quantity')
#         try:
#             session.modified = True
#             for key, item in session['shopcart'].items():
#                 if int(key) == code:
#                     item['quantity'] = quantity
#                     flash('Item Updated', 'success')
#                     return redirect(url_for('get_cart'))
#         except Exception as e:
#             print(e)
#             return redirect(url_for('get_cart'))
        
@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'shopcart' not in session or len(session['shopcart']) <= 0:
        return redirect(url_for('index'))
    try:
        session.modified = True
        for key, item in session['shopcart'].items():
            if int(key) == id:
                session['shopcart'].pop(key, None)
                return redirect(url_for('get_cart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getcart'))

@app.route('/clearcart')
def clearcart():
    try:
        session.pop('shopcart', None)
        return redirect(url_for('shop'))
    except Exception as e:
        print(e)


     


def is_valid(email, password):
    cur = conn
    cur.execute('SELECT email, password FROM users')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False
        

#Fetch user details if logged in
def getLoginDetails():
    if 'email' not in session:
        loggedIn = False
        firstname = ''
        noOfItems = 0
    else:
        loggedIn = True
        userId, firstname = db.session.query(userId, firstname)
        noOfItems = db.session.query(Cart.productId).count()
    db.session.close()
    return (loggedIn, firstname, noOfItems)
    

        
@app.route("/samplecart")
def samplecart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    with conn as cur:
        cur.execute("SELECT userId FROM users WHERE email = '" + email + "'")
        userId = cur.get().fetchone()[0]
        cur.execute("SELECT products.productId, products.name, products.price, products.image FROM products, kart WHERE products.productId = kart.productId AND kart.userId = " + str(userId))
        products = cur.fetchall()
    totalPrice = 0
    for row in products:
        totalPrice += row[2]
    return render_template("cart.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")
        
# @app.route("/checkout")
# def checkout():
#     if 'email' not in session:
#         return redirect(url_for('login'))
#     loggedIn, firstName, noOfItems = getLoginDetails()
#     email = session['email']
#     with conn as cur:
#         cur.execute("SELECT userId FROM users WHERE email = '" + email + "'")
#         userId = cur.fetchone()[0]
#         cur.execute("SELECT products.productId, products.name, products.price, products.image FROM products, kart WHERE products.productId = kart.productId AND kart.userId = " + str(userId))
#         products = cur.fetchall()
#     totalPrice = 0
#     for row in products:
#         totalPrice += row[2]
#     return render_template("checkout.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

        
@app.route("/removeFromCart")
def removeFromCart():
    if 'email' not in session:
        return redirect(url_for('login'))
    email = session['email']
    productId = int(request.args.get('productId'))
    with conn as cur:
        cur.execute("SELECT userId FROM users WHERE email = '" + email + "'")
        userId = cur.fetchone()[0]
        try:
            cur.execute("DELETE FROM kart WHERE userId = " + str(userId) + " AND productId = " + str(productId))
            cur.commit()
            flash("removed successfully", category='success')
        except:
            cur.rollback()
            flash("error occurred", category='error')
    cur.close()
    return redirect(url_for('index'))


@app.route("/logout")
def logout():
    session.pop('email', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))
        
            
@app.route("/productDescription")
def productDescription():
    loggedIn, firstName, noOfItems = getLoginDetails()
    productId = request.args.get('productId')
    with conn:
        conn.execute('SELECT productId, name, price, image, description, specification, reviews, category, brand, stock, categoryId FROM products WHERE productId = ' + productId)
        productData = conn.fetchone()
    conn.close()
    return render_template("shop_details.html", data=productData, loggedIn = loggedIn, firstName = firstName, noOfItems = noOfItems)

        
@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('index'))
    else:
        return render_template('loginreal.html', error='')
    
@app.route("/updateProfile", methods=["GET", "POST"])
def updateProfile():
    if request.method == 'POST':
        #Parse form data
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address = request.form['address']
        postalcode = request.form['postalcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phonenumber = request.form['phonenumber']
        with conn:
            try:
                conn.execute('UPDATE users SET firstName = ?, lastName = ?, address = ?, postalcode = ?, city = ?, state = ?, country = ?, phonenumber = ? WHERE email = ?', (firstName, lastName, address, postalcode, city, state, country, phonenumber, email))
                
                conn.commit()
                flash("Saved Successfully", category='success')
            except:
                conn.rollback()
                flash("Error occured", category='error')
    conn.close()
    return redirect(url_for('editProfile'))

@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def changePassword():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    if request.method == "POST":
        oldPassword = request.form['oldpassword']
        oldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
        newPassword = request.form['newpassword']
        newPassword = hashlib.md5(newPassword.encode()).hexdigest()
        with conn:
            conn.execute("SELECT userId, password FROM users WHERE email = '" + session['email'] + "'")
            userId, password = conn.fetchone()
            if (password == oldPassword):
                try:
                    conn.execute("UPDATE users SET password = ? WHERE userId = ?", (newPassword, userId))
                    conn.commit()
                    flash("Changed successfully", category="success")
                except:
                    conn.rollback()
                    flash("Failed, An error occurred!", category='error')
                return render_template("changePassword.html")
            else:
                flash("Wrong password", category='error')
        conn.close()
        return render_template("changePassword.html")
    else:
        return render_template("changePassword.html")
        
@app.route("/account/profile/edit")
def editProfile():
    if 'email' not in session:
        return redirect(url_for('index'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    with conn:
        conn.execute("SELECT userId, email, firstName, lastName, address, postalcode, city, state, country, phonenumber FROM users WHERE email = '" + session['email'] + "'")
        profileData = conn.fetchone()
    conn.close()
    return render_template("editProfile.html", profileData=profileData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/account/profile")
def profileHome():
    if 'email' not in session:
        return redirect(url_for('index'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    return render_template("profileHome.html", loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

#Display all items of a category
@app.route("/displayCategory")
def displayCategory():
        loggedIn, firstName, noOfItems = getLoginDetails()
        categoryId = request.args.get("categoryId")
        with conn:
            conn.execute("SELECT products.productId, products.name, products.price, products.image, categories.name FROM products, categories WHERE products.categoryId = categories.categoryId AND categories.categoryId = " + categoryId)
            data = conn.fetchall()
        conn.close()
        categoryName = data[0][4]
        data = parse(data)
        return render_template('displayCategory.html', data=data, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryName=categoryName)

def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans
        
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
        
if __name__ == '__main__':
    app.run(port=5000, debug=True)