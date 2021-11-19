from project import db
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    email = db.Column(db.String(30), unique=True)
    role = db.Column(db.String(30))
    password = db.Column(db.String(80))

class ProductRequest(db.Model):
    __tablename__ = "product_requests"
    productrequest_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    client_id = db.Column(db.Integer)
    shop_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    timestamp = db.Column(db.String(40))

class Client(db.Model):
    __tablename__ = "clients"
    client_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    wallet = db.Column(db.Float)

class Product(db.Model):
    __tablename__ = "products"
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    price = db.Column(db.Float)
    qty_available = db.Column(db.Integer)
    qty_requested = db.Column(db.Integer)
    farmer_id = db.Column(db.Integer)
    img_url = db.Column(db.String(50))