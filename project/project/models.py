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
    company = db.Column(db.String(40))
    wallet = db.Column(db.Float)

class ProductRequest(db.Model):
    __tablename__ = "product_requests"
    productrequest_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    client_id = db.Column(db.Integer)
    shop_id = db.Column(db.Integer)
    quantity = db.Column(db.Float)
    timestamp = db.Column(db.String(40))

class ProductInOrder(db.Model):
    __tablename__ = "product_in_order"
    pio_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    order_id = db.Column(db.Integer)
    quantity = db.Column(db.Float)
    confirmed = db.Column(db.Integer)

class ProductInBasket(db.Model):
    __tablename__ = "product_in_basket"
    pib_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    client_id = db.Column(db.Integer)
    quantity = db.Column(db.Float)

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
    description = db.Column(db.String(500))
    qty_available = db.Column(db.Float)
    qty_requested = db.Column(db.Float)
    farmer_id = db.Column(db.Integer)
    img_url = db.Column(db.String(50))
    date = db.Column(db.String(50))

class Order(db.Model):
    __tablename__ = "orders"
    order_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer)
    delivery_address = db.Column(db.String(100))
    home_delivery = db.Column(db.String(2))
    total = db.Column(db.Float)
    requested_delivery_date = db.Column(db.String(50))
    actual_delivery_date = db.Column(db.String(50))
    status = db.Column(db.String(20))
    # status is PENDING if the order has just been submitted,
    # status is ACCEPTED if the order is accepted from the farmer,
    # status is DELIVERING if the order is delivered from the farmer,
    # status is CANCELLED if the order has been cancelled (insufficient balance),
    # status is LODGED if the order has arrived to the pick-up point,
    # status is DELIVERED if the order has been handed out to the client.
    