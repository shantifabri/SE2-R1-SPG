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
    pending_amount = db.Column(db.Float)
    tg_chat_id = db.Column(db.String(50))

class ProductRequest(db.Model):
    __tablename__ = "product_requests"
    productrequest_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    client_id = db.Column(db.Integer)
    shop_id = db.Column(db.Integer)
    quantity = db.Column(db.Float)
    timestamp = db.Column(db.String(40))
    deleted = db.Column(db.Integer)

class ProductInOrder(db.Model):
    __tablename__ = "product_in_order"
    pio_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    order_id = db.Column(db.Integer)
    quantity = db.Column(db.Float)
    confirmed = db.Column(db.Integer)
    qty_confirmed = db.Column(db.Float)
    
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
    qty_confirmed = db.Column(db.Float)
    qty_warehousing = db.Column(db.Float)
    qty_warehoused = db.Column(db.Float)
    farmer_id = db.Column(db.Integer)
    img_url = db.Column(db.String(50))
    date = db.Column(db.String(50))
    deleted = db.Column(db.Integer) 

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
    order_date = db.Column(db.String(50))

    # status is PENDING if the order has just been submitted,
    # status is PENDING CANCELLATION if the wallet is not enough to pay the order,
    # status is CONFIRMED if the order is confirmed from the farmer,
    # status is WAREHOUSING if the order is delivered from the farmer to the warehouse,
    # status is WAREHOUSED if the order has been received from the farmer by the warehouse manager,
    # status is PREPARED if the warehouse worker has prepared the bag with the goods,
    # status is CANCELLED if the order has been cancelled (insufficient balance),
    # status is DELIVERING if the order has been delivered from the warehouse,
    # status is LODGED if the order has arrived to the pick-up point,
    # status is DELIVERED if the order has been handed out to the client or delivered to the client address.