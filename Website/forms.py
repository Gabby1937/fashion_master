from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, FloatField, IntegerField
from wtforms.validators import DataRequired, AnyOf, URL

# class VenueForm(FlaskForm):

# class ShowForm(FlaskForm):
    
    
    # productId SERIAL PRIMARY KEY,
    # name VARCHAR(255) NOT NULL,
    # price float(2) NOT NULL,
    # discount_percent INTEGER,
    # image_link VARCHAR(255) NOT NULL,
    # qty INTEGER NOT NULL,
    # video_link VARCHAR(255) NOT NULL,
    # colors VARCHAR(255) NOT NULL,
    # description VARCHAR(500) NOT NULL,
    # specification VARCHAR(300) NOT NULL,
    # ratings INTEGER NOT NULL,
    # reviews VARCHAR(255) NOT NULL,
    # category VARCHAR(255) NOT NULL,
    # brand VARCHAR(255) NOT NULL,
    # tags VARCHAR(255) NOT NULL,
    # size VARCHAR(255) NOT NULL
class ProductForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    price = FloatField(
        'price', validators=[DataRequired()]
    )
    discount = IntegerField(
        'discount', validators=[DataRequired()]
    )
    image_link = StringField(
        'image_link'
    )
    qty = IntegerField(
        'qty', validators=[DataRequired()]
    )
    video_link = StringField(
        'video_link'
    )
    color = SelectField(
        'color', validators=[DataRequired()],
        choices=[
            ('Red', 'Red'),
            ('Green', 'Green'),
            ('Blue', 'Blue'),
            ('Yellow', 'Yellow'),
            ('White', 'White'),
            ('Pink', 'Pink'),
            ('Purple', 'Purple'),
            ('Black', 'Black'),
            ('Gray', 'Gray'),
        ]
    )
    description = StringField(
        'description'
    )
    specification = StringField(
        'specification'
    )
    ratings = SelectField(
        'ratings', validators=[DataRequired()],
        choices=[
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
        ]
    )
    reviews = StringField(
        'reviews'
    )
    
    category = SelectMultipleField(
        'category', validators=[DataRequired()],
        choices=[
            ('Men', 'Men'),
            ('Women', 'Women'),
            ('Clothing', 'Clothing'),
            ('Bags', 'Bags'),
            ('Shoes', 'Shoes'),
            ('Accessories', 'Accessories'),
            ('Kids', 'Kids'),
        ]
    )
    brand = SelectMultipleField(
        'brand', validators=[DataRequired()],
        choices=[
            ('Hermes', 'Hermes'),
            ('Gucci', 'Gucci'),
            ('Fendi', 'Fendi'),
            ('Chanel', 'Chanel'),
            ('Louis Vuitton', 'Louis Vuitton'),
            ('Versace', 'Versace'),
            ('Palm Angels', 'Palm Angels'),
            ('Dior', 'Dior'),
            ('Balencieaga', 'Balencieaga'),
            ('Abba made', 'Abba made'),
        ]
    )
    tags = SelectMultipleField(
        'tags', validators=[DataRequired()],
        choices=[
            ('PRODUCT', 'PRODUCT'),
            ('SHOES', 'SHOES'),
            ('CLOTHES', 'CLOTHES'),
            ('BAGS', 'BAGS'),
            ('HATS', 'HATS'),
            ('FASHION', 'FASHION'),
            ('ACCESSORIES', 'ACCESSORIES'),
        ]
    )
    size = SelectField(
        'size', validators=[DataRequired()],
        choices=[
            ('4XL', '4XL'),
            ('3XL', '3XL'),
            ('XXL', 'XXL'),
            ('XL', 'XL'),
            ('L', 'L'),
            ('M', 'M'),
            ('S', 'S'),
            ('XS', 'XS'),
        ]
    )

class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )