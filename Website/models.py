import os
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey, PrimaryKeyConstraint
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.orm import relationship, sessionmaker
#from settings import db_name, db_user, db_password
import json
from flask_sqlalchemy import SQLAlchemy
#from flask_app import app
from flask_migrate import Migrate
from flask_moment import Moment
#from flask_script import Manager
import datetime
import psycopg2
from flask_login import login_required, UserMixin, current_user, LoginManager
from flask import Flask, render_template, redirect, request, session, jsonify, url_for, flash
#import psycopg2


# database_name = db_name
# database_path = 'postgres://{}:{}@{}/{}'.format(db_user, db_password, 'localhost:5432', database_name)
database_path = 'postgresql://master:ekka@localhost:5432/ekkadb'

app = Flask(__name__)
login_manager = LoginManager(app)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = database_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.app_context().push()

# engine = create_engine(database_path)
# Session = sessionmaker(engine)

# """
# setup_db(app)
#     binds a flask application and a SQLAlchemy service
# """
# def setup_db(app, database_path=database_path):
#     app.config["SQLALCHEMY_DATABASE_URI"] = database_path
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     db.app = app
#     db.init_app(app)
#     db.create_all()
# setup_db(app, database_path)


# connection = psycopg2.connect('postgresql://master:ekka@localhost:5432/ekkadb')

# cursor = connection.cursor()
connection = psycopg2.connect('postgresql://master:ekka@localhost:5432/ekkadb')
conn = connection.cursor()
# cursor.execute('''
#    CREATE TABLE table2 (
#        id INTEGER PRIMARY KEY,
#        completed BOOLEAN NOT NULL DEFAULT False
#    );
# ''')

# DROP TABLE messages;
#     CREATE TABLE messages (
#     id SERIAL PRIMARY KEY,
#     userId INT NOT NULL,
#     name TEXT NOT NULL,
#     email TEXT NOT NULL,
#     content TEXT NOT NULL,
#     CONSTRAINT fk_users FOREIGN KEY(userId) REFERENCES users(userId)
#     );


class Message(db.Model):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    content = Column(String)
    
    def __init__(self, name, email, content):
        self.name = name
        self.email = email
        self.content = content
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def format(self):
        return {
            'name' : self.name,
            'email' : self.email,
            'content' : self.content
        }
        
        
        
        
class Comment(db.Model):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    message = Column(String)
    
    def __init__(self, name, email, phone, message):
        self.name = name
        self.email = email
        self.phone = phone
        self.message = message
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def format(self):
        return {
            'name' : self.name,
            'email' : self.email,
            'phone': self.phone,
            'message' : self.message
        }
        
        
        
        
        
        
        
        

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    userid = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)
    password = Column(String)
    phonenumber = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    postalcode = Column(String)
    #carts = db.relationship('Cart', backref='users', lazy=True)
    #db.create_all()
    #cart = relationship("Kart")
    
    # def __repr__(self):
    #     return f"<Product {self.userid} name: {self.firstname}>"
    
    def __init__(self, firstname, lastname, email, password, phonenumber, address, city, state, country, postalcode):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.phonenumber = phonenumber
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.postalcode = postalcode
        #self.carts = carts
        
    def is_authenticated(self):
        return self.authenticated
    
    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def format(self):
        return {
            'userid': self.userid,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'password': self.password,
            'phonenumber': self.phonenumber,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'postalcode': self.postalcode,
            #'carts': self.carts,
            }
        

def load_user(userid):
    userid = conn.execute("select userid from users where email = '{}'".format(user_email))
    userid = conn.fetchone()
    return User.query.get(userid)
        
#     CREATE TABLE products(
#     productId SERIAL PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     price float(2) NOT NULL,
#     discount_percent INTEGER,
#     image_link1 VARCHAR(255) NOT NULL,
#     image_link2 VARCHAR(255) NOT NULL,
#     image_link3 VARCHAR(255) NOT NULL,
#     image_link4 VARCHAR(255) NOT NULL,
#     image_link5 VARCHAR(255) NOT NULL,
#     description VARCHAR(500) NOT NULL,
#     specification VARCHAR(300) NOT NULL,
#     ratings INTEGER NOT NULL,
#     reviews VARCHAR(255) NOT NULL,
#     category VARCHAR(255) NOT NULL,
#     brand VARCHAR(255) NOT NULL,
#     qty INTEGER NOT NULL,
#     tags VARCHAR(255) NOT NULL,
#     carts VARCHAR(255) NOT NULL,
#     video_link VARCHAR(255) NOT NULL,
#     colors VARCHAR(255) NOT NULL,
#     size VARCHAR(255) NOT NULL
# );


# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     price = db.Column(db.Numeric(10,2), nullable=False)
#     stock = db.Column(db.Integer, nullable=False)
#     desc = db.Column(db.Text, nullable=False)
#     pub_date = db.Column(db.DateTime, nullable=False,default=datetime.now())
#     brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=False)
#     brand = db.relationship('Brand', backref=db.backref('brand', lazy=True))
#     category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
#     category = db.relationship('Category' , backref=db.backref('category', lazy=True))

#     image_1 = db.Column(db.String(256), nullable=False, default='image1.jpg')

#     def __repr__(self):
#         return '<Product %r>' % self.name

# class Brand(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), nullable=False, unique=True)

# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), nullable=False, unique=True)
def discount_price(price, percent):
    result = (price * percent) / 100
    x = price - result
    return x






class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    percent = db.Column(db.Integer, nullable=False)
    image_link1 = db.Column(db.String(120))
    image_link2 = db.Column(db.String(120))
    image_link3 = db.Column(db.String(120))
    image_link4 = db.Column(db.String(120))
    image_link5 = db.Column(db.String(120))
    description = db.Column(db.Text, nullable=False)
    specification = db.Column(db.Text, nullable=False)
    ratings = db.Column(db.Integer, nullable=False)
    reviews = db.Column(db.Text, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    tags = db.Column(db.String(350), nullable=False)
    video_link = db.Column(db.String(120))
    colors = db.Column(db.String(350), nullable=False)
    size = db.Column(db.String(350), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=False)
    brand = db.relationship('Brand', backref=db.backref('brand', lazy=True))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category' , backref=db.backref('category', lazy=True))
    
    # def __repr__(self):
    #     return '<Product %r>' % self.name
    def __init__(self, name, price, percent, image_link1,
                image_link2, image_link3, image_link4,
                image_link5, description, specification, ratings,
                reviews, category_id, brand_id, qty, tags, video_link, colors, size):
        self.name = name
        self.price = price
        self.percent = percent
        self.image_link1 = image_link1
        self.image_link2 = image_link2
        self.image_link3 = image_link3
        self.image_link4 = image_link4
        self.image_link5 = image_link5
        self.description = description
        self.specification = specification
        self.ratings = ratings
        self.reviews = reviews
        self.category_id = category_id
        self.brand_id = brand_id
        self.qty = qty
        self.tags = tags
        #self.carts = carts
        self.video_link = video_link
        self.colors = colors
        self.size = size
        
    # def insert(self):
    #     db.session.add(self)
    #     db.session.commit()

    # def update(self):
    #     db.session.commit()

    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()
        
    # def format(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'price': self.price,
    #         'percent': self.percent,
    #         'discount': self.discount,
    #         'image_link1': self.image_link1, 
    #         'image_link2': self.image_link2,
    #         'image_link3': self.image_link3, 
    #         'image_link4': self.image_link4, 
    #         'image_link5': self.image_link5,
    #         'description': self.description,
    #         'specification': self.specification,
    #         'ratings': self.ratings, 
    #         'reviews': self.reviews,
    #         'category_id': self.category_id,
    #         'brand_id': self.brand_id,
    #         'qty': self.qty,
    #         'tags': self.tags,
    #         #'carts': self.carts,
    #         'video_link': self.video_link,
    #         'colors': self.colors,
    #         'size': self.size,
    #     }
        
        
    

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    
    def __init__(self, name):
        self.name = name
    
    # def insert(self):
    #     db.session.add(self)
    #     db.session.commit()

    # def update(self):
    #     db.session.commit()

    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()
        
    # def format(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name
    #     }
        
    
    
        

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    
    def __init__(self, name):
        self.name = name
    
    # def insert(self):
    #     db.session.add(self)
    #     db.session.commit()

    # def update(self):
    #     db.session.commit()

    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()
        
    # def format(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name
    #     }
    
# CREATE TABLE products(
#     productId SERIAL PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     price float(2) NOT NULL,
#     discount_percent INTEGER,
#     image_link1 VARCHAR(255),
#     image_link2 VARCHAR(255),
#     image_link3 VARCHAR(255),
#     image_link4 VARCHAR(255),
#     image_link5 VARCHAR(255),
#     description VARCHAR(500) NOT NULL,
#     specification VARCHAR(300) NOT NULL,
#     ratings INTEGER NOT NULL,
#     reviews VARCHAR(255) NOT NULL,
#     category_id VARCHAR(255),
#     brand VARCHAR(255) NOT NULL,
#     qty INTEGER NOT NULL,
#     tags VARCHAR(255) NOT NULL,
#     carts VARCHAR(255),
#     video_link VARCHAR(255),
#     colors VARCHAR(255) NOT NULL,
#     size VARCHAR(255) NOT NULL
# );
    
    # def __repr__(self):
    #     return f"<Product {self.productid} name: {self.name}>"

     
    # def __init__(self, name, price, percent, image_link1,
    #              image_link2, image_link3, image_link4,
    #              image_link5, description, specification, ratings,
    #              reviews, category_id, brand, qty, tags, video_link, colors, size):
    #     self.name = name
    #     self.price = price
    #     self.percent = percent
    #     self.image_link1 = image_link1
    #     self.image_link2 = image_link2
    #     self.image_link3 = image_link3
    #     self.image_link4 = image_link4
    #     self.image_link5 = image_link5
    #     self.description = description
    #     self.specification = specification
    #     self.ratings = ratings
    #     self.reviews = reviews
    #     self.category_id = category_id
    #     self.brand = brand
    #     self.qty = qty
    #     self.tags = tags
    #     #self.carts = carts
    #     self.video_link = video_link
    #     self.colors = colors
    #     self.size = size
        
    
    # def insert(self):
    #     db.session.add(self)
    #     db.session.commit()

    # def update(self):
    #     db.session.commit()

    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()
        
    # def format(self):
    #     return {
    #         'name': self.name,
    #         'price': self.price,
    #         'percent': self.percent,
    #         'image_link1': self.image_link1, 
    #         'image_link2': self.image_link2,
    #         'image_link3': self.image_link3, 
    #         'image_link4': self.image_link4, 
    #         'image_link5': self.image_link5,
    #         'description': self.description,
    #         'specification': self.specification,
    #         'ratings': self.ratings, 
    #         'reviews': self.reviews,
    #         'category_id': self.category_id,
    #         'brand': self.brand,
    #         'qty': self.qty,
    #         'tags': self.tags,
    #         #'carts': self.carts,
    #         'video_link': self.video_link,
    #         'colors': self.colors,
    #         'size': self.size,
    #     }
    

# class Category(db.Model):
#     __tablename__ = 'categories'

#     categoryId = db.Column(db.Integer, primary_key=True)
#     type = db.Column(db.String)
#     product = db.relationship('Product', backref='Category', lazy=True)
    
#     def __repr__(self):
#         return f"<Category {self.categoryId} type: {self.type}>"

#     def __init__(self, type, product):
#         self.type = type
#         self.product = product

#     def format(self):
#         return {
#             'categoryId': self.categoryId,
#             'type': self.type,
#             'product': self.product
#             }

# CREATE TABLE carts(
#     id SERIAL PRIMARY KEY,
#     name,
#     price,
#     quantity,
#     size,
#     colors,
#     image_link1,
#     category_id, 
#     brand_id, 
#     product_id
# );

class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(350), nullable=False)
    colors = db.Column(db.String(350), nullable=False)
    image_link1 = db.Column(db.String(120))
    product_id = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Numeric(10,2), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.userid'),nullable=False)
    user = db.relationship('User', backref=db.backref('users', lazy=True))
    
    def __init__(self, name, price, product_id, image_link1, qty, colors, size, total, user_id):
        self.name = name
        self.price = price
        self.image_link1 = image_link1
        self.qty = qty
        self.colors = colors
        self.size = size
        self.product_id = product_id
        self.total = total
        self.user_id = user_id
    


    
db.create_all()   
# db.create_all()

