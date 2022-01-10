from flask import render_template, request, flash, redirect, url_for, session, jsonify
from flask_login import login_user, current_user, login_required, logout_user

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import func,or_,and_
from wtforms.fields import datetime
from sqlalchemy.sql import text
import os
import json
import base64
from dotenv import load_dotenv, find_dotenv
from project.other.utils import mail_sender
from project.models import User, Product, Client, ProductRequest, ProductInOrder, ProductInBasket, Order
from project.forms import ProductSearch, ProductRequestForm, ClientInsertForm, AddToCartForm, TopUpForm, CheckOutForm, TopUpSearch, ProductInsertForm, ProductEditForm, CheckOutClientForm
from project import db
import datetime
import sendgrid
from sendgrid.helpers.mail import *

from . import other_blueprint

from telepot.loop import MessageLoop
import telepot
import time
import socket

load_dotenv(verbose=True)
TOKEN = os.getenv("TOKEN")
bot = telepot.Bot(TOKEN)

#### routes ####
@other_blueprint.route('/')
def index():
    return render_template('index.html')

@other_blueprint.route('/products', methods=['GET','POST'])
def products():
    # if current_user.role != 'S' and current_user.role != 'C' and current_user.role != 'F':
    #     return redirect(url_for('other.index'))
    form = ProductSearch()
    products = db.session.query(
        Product, 
        User
        ).filter(
            User.id == Product.farmer_id
        ).filter(
            Product.deleted == 0
        ).all()
    if form.validate_on_submit():
        if form.search.data == None:
            search = ""
        products = db.session.query(
            Product,
            User
        ).filter(
            User.id == Product.farmer_id
        ).filter(

            or_(Product.name.like("%" + form.search.data + "%"),User.company.like("%" + form.search.data + "%"))
        ).filter(
            Product.deleted == 0
        ).all()
    
    return render_template('products.html',products=products,form=form)

@other_blueprint.route('/singleproduct/<product_id>',  methods=['GET','POST'])
def singleproduct(product_id):
    # if current_user.role != 'S' and current_user.role != 'C' and current_user.role != 'F':
    #     return redirect(url_for('other.index'))
    time = "ZZZZ:ZZZZ:ZZ:ZZ zz ZZ"
    form = AddToCartForm()
    product = db.session.query(
        Product,
        User
        ).filter(
            Product.product_id == product_id
        ).filter(
            User.id == Product.farmer_id
        ).all()[0]
    if form.validate_on_submit():
        try:
            productReq = ProductInBasket(product_id=product[0].product_id, client_id=current_user.id, quantity=form.quantity.data)
            db.session.add(productReq)
            db.session.commit()
            status_counts = db.session.query(ProductInBasket.client_id, db.func.count(ProductInBasket.product_id).label('count_id')
                ).filter(ProductInBasket.client_id == current_user.id).group_by(ProductInBasket.pib_id
                ).all()
            session["cart_count"] = len(status_counts)

            return redirect(url_for('other.products'))
        except Exception as e:
            print(e)
            return render_template('singleproduct.html', product=product, form=form, valid=False)
    return render_template('singleproduct.html', product=product, form=form, valid=True)

@other_blueprint.route('/insertclient', methods=['GET','POST'])
def insertclient():
    # if current_user.role != 'S':
    #     return redirect(url_for('other.index'))
    # name, surname, email, phone, wallet
    time = "ZZZZ:ZZZZ:ZZ:ZZ zz ZZ"
    form = ClientInsertForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        # add the user form input which is form.'field'.data into the column which is 'field'
        new_user = User(name=form.name.data, surname=form.surname.data, role='C', email=form.email.data, password=hashed_password, company="Client", wallet=0, pending_amount=0, tg_chat_id=form.Telegram_id.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('other.index'))

    return render_template('insertclient.html', form=form)

@other_blueprint.route('/updatequantity/<pib_id>/<amount>',  methods=['GET','POST'])
@login_required
def updatequantity(pib_id,amount):
    if current_user.role != 'S' and current_user.role != 'C':
        return redirect(url_for('other.index'))
    amount = float(amount)
    pib_id = int(pib_id)
    if amount != 0:
        a_user = db.session.query(ProductInBasket).filter(ProductInBasket.pib_id == pib_id).one()
        a_user.quantity = amount
        db.session.commit()
    else:
        ProductInBasket.query.filter_by(pib_id=pib_id).delete()
        db.session.commit()
        status_counts = db.session.query(ProductInBasket.client_id, db.func.count(ProductInBasket.product_id).label('count_id')
                ).filter(ProductInBasket.client_id == current_user.id).group_by(ProductInBasket.pib_id
                ).all()
        session["cart_count"] = session["cart_count"] = len(status_counts)

    return redirect(url_for('other.shoppingcart'))

@other_blueprint.route('/updateshipping/<value>',  methods=['GET','POST'])
@login_required
def updateshipping(value):
    if current_user.role != 'S' and current_user.role != 'C':
        return redirect(url_for('other.index'))

    if value == "home":
        session["shipping"] = '%.2f' % 7.50
    else:
        session["shipping"] = 0

    return redirect(url_for('other.shoppingcart'))

@other_blueprint.route('/confirmarrivals', methods=['GET', 'POST'])
@login_required
def confirmarrivals():
    farmers = db.session.query(ProductInOrder,Product,User,Order
    ).filter(
        and_(Order.order_id == ProductInOrder.order_id, ProductInOrder.product_id == Product.product_id, Product.farmer_id == User.id, ProductInOrder.confirmed == 1)
    ).group_by(
        User.id,User.name,User.surname,User.company
    ).all()
    products = db.session.query(Product
    ).filter(
        Product.qty_confirmed>0
    ).filter(
        Order.status == "CONFIRMED"
    ).group_by(
        Product.farmer_id,Product.product_id
    ).all()
    farmerproducts = {}
    for product in products:
        if product.farmer_id in farmerproducts.keys():
            farmerproducts[product.farmer_id].append({'name':product.name, 'quantity':product.qty_confirmed, 'id':product.product_id})
        else:
            farmerproducts[product.farmer_id]=[]
            farmerproducts[product.farmer_id].append({'name':product.name, 'quantity':product.qty_confirmed, 'id':product.product_id})

    return render_template('confirmarrivals.html', farmers=farmers, farmerproducts=farmerproducts)

@other_blueprint.route('/deleteproduct/<product_id>',  methods=['GET','POST'])
@login_required
def deleteproduct(product_id):
    product = db.session.query(Product).filter(Product.product_id == product_id).one()
    product.deleted = 1
    db.session.commit()
    return redirect(url_for('other.manageproducts'))

@other_blueprint.route('/updatestatus/<order_id>/<status>/<redirect_url>',  methods=['GET','POST'])
@login_required
def updatestatus(order_id,status,redirect_url):
    order = db.session.query(Order).filter(Order.order_id == order_id).one()
    user = db.session.query(User).filter(User.id == order.client_id).one()
    order.status = status
    if status == "DELIVERING":
        subject = "Order Delivering"
        msg = "Dear "+user.name+", your order with id: #"+str(order.order_id)+",\nfor a total price of: €"+str(order.total)+",\nis being delivered to the chosen delivery place ("+order.delivery_address+").\nMake sure to not miss your delivery!\nThanks, \nSPG Team."
        mail_sender(subject,msg,user.email)
        order.actual_delivery_date = session.get("date")

    db.session.commit()
    redirect_url = "other." + str(redirect_url)
    return redirect(url_for(redirect_url))

@other_blueprint.route('/confirmwarehousing/<product_id>/<quantity>',  methods=['GET','POST'])
@login_required
def confirmwarehousing(product_id,quantity):

    product = db.session.query(Product).filter(Product.product_id == product_id).one()
    print(quantity)
    
    product.qty_warehousing += float(quantity)

    products = db.session.query(
        ProductInOrder,Order
        ).filter(
            ProductInOrder.order_id == Order.order_id
        ).filter(
            ProductInOrder.product_id == product_id
        ).filter(
            Order.status == "CONFIRMED"
        ).filter(
            ProductInOrder.confirmed == 1
        ).all()
    
    for p in products:
        p[0].confirmed=2
    
    db.session.commit()

    p1 = db.session.query(
        Order
    ).filter(
            Order.status == "CONFIRMED"
    ).all()

    for ps1 in p1:
        p2 = db.session.query(
            ProductInOrder
        ).filter(
            ProductInOrder.order_id == ps1.order_id
        ).all()
        
        f = True
    
        for ps2 in p2:
            if ps2.confirmed == 1:
                f=False
                
        if f == True:
            ps1.status = "WAREHOUSING"

    db.session.commit()
    return redirect(url_for('other.farmerconfirmation'))

@other_blueprint.route('/confirmorder/<order_id>/<pio_id>/<product_id>/<quantity>',  methods=['GET','POST'])
@login_required
def confirmorder(order_id,pio_id,product_id,quantity):
    confirm_order(order_id,pio_id,product_id,quantity)
    return redirect(url_for('other.farmerorders'))

def confirm_order(order_id,pio_id,product_id,quantity):
    order = db.session.query(Order).filter(Order.order_id == order_id).one()
    pio = db.session.query(ProductInOrder).filter(ProductInOrder.pio_id == pio_id).one()
    product = db.session.query(Product).filter(Product.product_id == product_id).one()
    user = db.session.query(User,Order).filter(User.id == Order.client_id).filter(Order.order_id == order_id).one()
    # order.status = status
    qty_remaining = product.qty_available - product.qty_confirmed
    print(quantity)
#    if pio.quantity > qty_remaining:
#        pio.quantity = qty_remaining
    if float(quantity) > qty_remaining:
        pio.qty_confirmed = qty_remaining
    else:
        pio.qty_confirmed = float(quantity)
    product.qty_confirmed += pio.qty_confirmed
    pio.confirmed = 1
    
    products = db.session.query(
        ProductInOrder
        ).filter(
            ProductInOrder.order_id == order_id
        ).filter(
            ProductInOrder.confirmed == 0
        ).all()
    if len(products) == 0:
        #FIXME send email when order is confirmed
        items = db.session.query(ProductInOrder).filter(ProductInOrder.order_id == order.order_id).all()
        old_total = order.total
        if order.home_delivery == 'N':
            new_total = 0
        else:
            new_total = 7.50
        for item in items:
            prod = db.session.query(Product).filter(Product.product_id == item.product_id).one()
            new_total += prod.price * item.qty_confirmed
            print(item.qty_confirmed)
            # item.confirmed = False
        order.total = new_total

        if order.total == 0 or (order.home_delivery != 'N' and order.total == 7.50):
            order.status = "CANCELLED"
        
        else:
            if order.status == "PENDING CANCELLATION":
                pass

            else:
                order.status = 'CONFIRMED'
                user[0].wallet -= new_total
                user[0].pending_amount -= old_total

        try:
            bot.sendMessage(chat_id=user[0].tg_chat_id, text='Your order number:%d is confirmed' % (order.order_id))
        except telepot.exception.TelegramError:
            bot.sendMessage(chat_id=473918518, text='User: %s order is confirmed but Telegram message sent failed'%(user[0].email))

    db.session.commit()

@other_blueprint.route('/shoppingcart', methods=['GET','POST'])
def shoppingcart():
    if current_user.role != 'S' and current_user.role != 'C':
        return redirect(url_for('other.index'))
    
    
    if current_user.role == "C":
        form = CheckOutClientForm()
        form.email.data = current_user.email
    else:
        form = CheckOutForm()
    
    
    if session.get("shipping",0) == 0:
        form.delivery_address.data = "Store"
        
    session["shipping"] = session.get("shipping",0)
    q = db.session.query(
        ProductInBasket, 
        Product, 
        User
        ).filter(
            User.id == Product.farmer_id
        ).filter(
            ProductInBasket.product_id == Product.product_id
        ).filter(
            ProductInBasket.client_id == current_user.id
        ).all()
    vals = {}
    products = []
    total = 0
    for val in q:
        prod = {}
        prod["product_id"] = val[1].product_id
        prod["pib_id"] = val[0].pib_id
        prod["farmer"] = val[2].company
        prod["price"] = '%.2f' % (val[0].quantity * val[1].price)
        prod["quantity"] = val[0].quantity
        prod["name"] = val[1].name
        prod["url"] = val[1].img_url
        prod["id"] = val[0].pib_id
        prod["qty_available"] = val[1].qty_available - val[1].qty_requested
        total += val[0].quantity * val[1].price
        products.append(prod)
    vals["subtotal"] = '%.2f' % total
    vals["products"] = products
    vals["total"] = '%.2f' % (total + float(session.get("shipping",0)))


    if form.validate_on_submit() and request.method == "POST":
        if form.date.data == "":
            return render_template('shoppingcart.html', values=vals, form=form, valid=True, date=False)
        q2 = db.session.query(
        User
        ).filter(
            User.email == form.email.data
        ).filter(
            User.role == "C"
        ).first()
        
        if q2 == None:
            return render_template('shoppingcart.html', values=vals, form=form, valid=False, date=True, balance=True)
        else:
            if session.get("shipping",0) == 0:
                address = "Store"
                home_delivery = "N"
            else:
                address = form.delivery_address.data
                home_delivery = "F"

            if address != None:
                balance = True
                if float(vals["total"]) > q2.wallet - q2.pending_amount:
                    balance = False
                    new_order = Order(client_id=q2.id, delivery_address=address, home_delivery=home_delivery, total=vals["total"], requested_delivery_date=form.date.data, actual_delivery_date="", status="PENDING CANCELLATION", order_date=session.get("date"))
                else:
                    new_order = Order(client_id=q2.id, delivery_address=address, home_delivery=home_delivery, total=vals["total"], requested_delivery_date=form.date.data, actual_delivery_date="", status="PENDING", order_date=session.get("date"))
                    q2.pending_amount = q2.pending_amount + float(vals["total"])
                # When a new order is added, the amount must be added to the pending amount.
                db.session.add(new_order)
                db.session.commit()
                ProductInBasket.query.filter_by(client_id=current_user.id).delete()

                items = []
                for prod in products:
                    items.append(ProductInOrder(product_id=prod["product_id"], quantity=prod["quantity"], order_id=new_order.order_id, confirmed=0, qty_confirmed=0))
                    product = db.session.query(Product).filter(Product.product_id == prod["product_id"]).first()
                    product.qty_requested = product.qty_requested + prod["quantity"]
                    db.session.commit()
                db.session.bulk_save_objects(items)
                db.session.commit()
                status_counts = db.session.query(ProductInBasket.client_id, db.func.count(ProductInBasket.product_id).label('count_id')
                    ).filter(ProductInBasket.client_id == current_user.id).group_by(ProductInBasket.pib_id
                    ).all()
                session["cart_count"] = len(status_counts)

                if not balance:
                    # Send an email to the user to remind to top-up the wallet
                    subject = "Insufficient Balance Reminder"
                    msg = "Dear User, your balance is €" + str(round(q2.wallet-q2.pending_amount,2)) + " and is not sufficient to complete the order #"+str(new_order.order_id)+" with a total of €"+str(new_order.total)+",\nPlease make sure to charge your wallet. Thanks, \nSPG Team."
                    mail_sender(subject,msg,q2.email)

                    i = 1
                    try:
                        while 1:
                            bot.sendMessage(chat_id=q2.tg_chat_id, text='%s' % (msg))
                            time.sleep(10)
                            # sleep 10s here just for test
                            i += 1
                            if i > 3:
                                break
                    except telepot.exception.TelegramError:
                        bot.sendMessage(chat_id=473918518, text='User: %s order failed notification sent failed' % (q2.email))
                    return render_template('shoppingcart.html', values={}, form=form, valid=True, date=True, balance=balance)

                return redirect(url_for('other.index'))
                # order_id = new_order.order_id

    return render_template('shoppingcart.html', values=vals, form=form, valid=True, date=True, balance=True)

@other_blueprint.route('/manageclients', methods=['GET','POST'])
@login_required
def manageclients():
    if current_user.role != 'S':
        return redirect(url_for('other.index'))
    return render_template('manageclients.html')

@other_blueprint.route('/insertproducts', methods=['GET','POST'])
@login_required
def insertproducts():
    if current_user.role != 'F':
        return redirect(url_for('other.index'))
    return render_template('insertproduct.html')

@other_blueprint.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    # if current_user.role != 'C':
    #     return redirect(url_for('other.index'))
    return render_template('profile.html')

@other_blueprint.route('/shoporders', methods=['GET', 'POST'])
@login_required
def shoporders():
    if current_user.role != 'S':
        return redirect(url_for('other.index'))
    orders = db.session.query(
        Order,  
        User
        ).filter(
            User.id == Order.client_id
        ).all()
    return render_template('shoporders.html', orders=orders)

@other_blueprint.route('/topup', methods=['GET','POST'])
@login_required
def topup():
    if current_user.role != 'S':
        return redirect(url_for('other.index'))
    form = TopUpForm()
    form_search = TopUpSearch()
    users = db.session.query(
        User
    ).filter(
        User.role == "C"
    ).all()

    if form.validate_on_submit():
        user = db.session.query(
            User
        ).filter(User.email == form.email.data
        ).one()
        user.wallet += form.amount.data
        try:
            bot.sendMessage(chat_id=user.tg_chat_id,text='Your wallet topped up with %s euro' % (form.amount.data))
        except telepot.exception.TelegramError:
            bot.sendMessage(chat_id=473918518,text='User: %s topped up successfully but Telegram message sent failed'%(user.email))
            # chat_id=473918518 can set as manager's userid. So manager can receive message when topup successful but
            # telegram sent failed.

        found = True
        while(found == True):
            order = db.session.query(
                Order
            ).filter(
                user.id == Order.client_id
            ).filter(
                Order.status == "PENDING CANCELLATION"
            ).filter(
                Order.total <= (user.wallet - user.pending_amount)
            ).all()
            # print(order)
            if len(order) > 0:
                prod_in_order = db.session.query(
                    ProductInOrder
                ).filter(
                    ProductInOrder.order_id == order[0].order_id
                ).filter(
                    ProductInOrder.confirmed == 0).all()
                
                if len(prod_in_order) > 0:
                    order[0].status = "PENDING"
                    user.pending_amount += order[0].total
                else:
                    order[0].status = "CONFIRMED"
                    user.wallet -= order[0].total
            else:
                found = False
        db.session.commit()

    if form_search.validate_on_submit():
        search = form_search.search.data
        if search == None:
            search = ""
        users = db.session.query(
            User
        ).filter(
            User.role == "C"
        ).filter(
            User.email.like("%" + search + "%")
        ).all()
    return render_template('topup.html', form=form, form_search=form_search, users=users)


@other_blueprint.route('/manageproducts', methods=['GET','POST'])
@login_required
def manageproducts():
    if current_user.role != 'F':
        return redirect(url_for('other.index'))
    form = ProductInsertForm()
    form_edit = ProductEditForm()
    products = db.session.query(
        Product
    ).filter(
        Product.farmer_id == current_user.id
    ).filter(
        Product.deleted == 0
    ).all()

    if form.validate() and request.method == "POST":
        filename = form.image.data.filename
        filenames = filename.split(".")
        prods = db.session.query(
            Product
        ).all()
        filename = filenames[0] + str(len(prods)) + "." + filenames[1]
        form.image.data.save("project/static/shop_imgs/" + filename)
        new_product = Product(name=form.name.data,price=form.price.data,description=form.description.data,qty_available=form.qty_available.data,qty_requested=0,qty_confirmed=0,qty_warehoused=0,farmer_id=current_user.id,img_url=filename,date=session.get("date",datetime.datetime.now()), deleted=0)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('other.manageproducts'))
    
    if form_edit.validate() and request.method == "POST":
        db.session.query(
            Product
        ).filter(Product.product_id == form_edit.product_id.data
        ).update({"name": (form_edit.name.data),"description": (form_edit.description.data),"price": (form_edit.price.data),"qty_available": (form_edit.qty_available.data)})
        db.session.commit()
        print(form_edit.name.data)
        print(form_edit.qty_available.data)
        print(form_edit.product_id.data)

        sendupdate = db.session.query(
            User.tg_chat_id
        ).filter(
            User.tg_chat_id > 0
        ).all()

        # for telegram link, need to attention the host!
        hostip = socket.gethostbyname(socket.gethostname())
        for sendid in sendupdate:
            print(sendid[0])
            try:
                bot.sendMessage(chat_id=sendid[0], text='Product is updated: %s, now available quantity is %s Kg, If you want to get more details, please click following link: http://%s:5000/singleproduct/%s' % (form_edit.name.data, form_edit.qty_available.data, hostip,  form_edit.product_id.data))
            except telepot.exception.TelegramError:
                bot.sendMessage(chat_id=473918518, text='Message notification sent failed to telegram user_id: %s .' % (sendid[0]))
    
    return render_template('manageproducts.html', products=products, form=form, form_edit=form_edit)

@other_blueprint.route('/farmerorders', methods=['GET', 'POST'])
@login_required
def farmerorders():
    if current_user.role != 'F':
        return redirect(url_for('other.index'))

    orders = db.session.query(Order,ProductInOrder,Product,User
    ).filter(
        Order.order_id == ProductInOrder.order_id
    ).filter(
        ProductInOrder.product_id == Product.product_id
    ).filter(
        Order.client_id == User.id
    ).filter(
        Product.farmer_id == current_user.id
    ).filter(
        or_(Order.status == "PENDING", Order.status == "PENDING CANCELLATION")
    # ).filter(
    #     ProductInOrder.confirmed == False
    ).all()
    return render_template('farmerorders.html', orders=orders)

@other_blueprint.route('/clientorders', methods=['GET', 'POST'])
@login_required
def clientorders():
    if current_user.role != 'C':
        return redirect(url_for('other.index'))

    client_orders = {}
    prod = {}
    orders = db.session.query(
        Order,  
        User,  
        ProductInOrder,
        Product
        ).filter(
            User.id == Product.farmer_id
        ).filter(
            Order.client_id == current_user.id
        ).filter(
            ProductInOrder.product_id == Product.product_id
        ).filter(
            ProductInOrder.order_id == Order.order_id
        ).all()
    order_query = db.session.query(
        Order,  
        User,  
        ProductInOrder,
        Product
        ).filter(
            User.id == Product.farmer_id
        ).filter(
            Order.client_id == current_user.id
        ).filter(
            ProductInOrder.product_id == Product.product_id
        ).filter(
            ProductInOrder.order_id == Order.order_id
        ).statement

    for order in orders:
        prod = {}
        id = str(order[0].order_id)
        # print(id + " " + order[3].name + " " + str(order[2].quantity))
        prod["name"] = str(order[3].name)
        prod["product_id"] = order[3].product_id
        prod["price"] = str(order[3].price)
        prod["qty_available"] = order[3].qty_available
        prod["qty_requested"] = order[3].qty_requested
        prod["qty_confirmed"] = order[3].qty_confirmed
        prod["order_qty"] = str(order[2].quantity)
        prod["farmer"] = order[1].company
        prod["img_url"] = order[3].img_url

        if id in list(client_orders.keys()):
            client_orders[id]["Products"].append(prod)
        else:
            # print("NEW")
            client_orders[id] = {}
            client_orders[id]["Order"] = order[0]
            client_orders[id]["Products"] = []
            client_orders[id]["Products"].append(prod)
        # print(client_orders[id]["Products"])
        # print(client_orders[order[0].order_id]["Products"])
        # print(prod)
        # print(client_orders[id])
    # print(client_orders)
    return render_template('clientorders.html', orders=orders, client_orders=client_orders)

@other_blueprint.route('/managerorders', methods=['GET', 'POST'])
@login_required
def managerorders():
    if current_user.role != 'M':
        return redirect(url_for('other.index'))
    orders = db.session.query(
        Order,  
        User
        ).filter(
            User.id == Order.client_id
        ).filter(
            or_(Order.status == "PREPARED", Order.status == "DELIVERING")
        ).all()

    return render_template('managerorders.html', orders=orders)

@other_blueprint.route('/sendmail/<email>/<subject>/<msg>/<redirecting>', methods=['GET', 'POST'])
@login_required
def sendmail(email,subject,msg,redirecting):
    load_dotenv(verbose=True)
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    print("API KEY : " + SENDGRID_API_KEY)
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    from_email = Email("Solidarity.purchase@gmail.com")
    to_email = To(email)
    content = Content("text/plain", msg)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return redirect(url_for('other.' + redirecting))

@other_blueprint.route('/workerorders', methods=['GET', 'POST'])
@login_required
def workerorders():
    if current_user.role != 'W':
        return redirect(url_for('other.index'))
    orders = db.session.query(
        Order,  
        User
        ).filter(
            User.id == Order.client_id
        ).filter(
            or_(Order.status == "WAREHOUSED",Order.status == "PREPARED")
        ).all()
    return render_template('workerorders.html', orders=orders)


@other_blueprint.route('/farmerconfirmation', methods=['GET', 'POST'])
def farmerconfirmation():
    if current_user.role != 'F':
        return redirect(url_for('other.index'))
    products = db.session.query(Product,ProductInOrder,User,Order,func.sum(ProductInOrder.quantity).label('quantity')
    ).filter(
        and_(User.id==Product.farmer_id,ProductInOrder.product_id==Product.product_id,Order.order_id==ProductInOrder.order_id,Order.status=='CONFIRMED',Product.farmer_id==current_user.id,Product.qty_warehousing<Product.qty_confirmed)
    ).group_by(
        Product.product_id,Product.name,Product.img_url,Product.price
    ).all()
    print(products)
    
    return render_template('farmerconfirmation.html',products=products)

@other_blueprint.route('/farmerorderconfirm', methods=['GET', 'POST'])
def farmerorderconfirm():
    if current_user.role != 'M':
        return redirect(url_for('other.index'))
    form = ProductInsertForm()
    form_edit = ProductEditForm()
    products = db.session.query(
        Product
    ).filter(
        Product.farmer_id == 9
    ).all()

    if form.validate() and request.method == "POST":
        # filename = secure_filename(form.image.data.filename)
        filename = form.image.data.filename
        filenames = filename.split(".")
        prods = db.session.query(
            Product
        ).all()
        filename = filenames[0] + str(len(prods)) + "." + filenames[1]
        form.image.data.save("project/static/shop_imgs/" + filename)
        new_product = Product(name=form.name.data,price=form.price.data,description=form.description.data,qty_available=form.qty_available.data,qty_requested=0,farmer_id=current_user.id,img_url=filename,date=session.get("date",datetime.datetime.now()))
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('other.manageproducts'))
    
    if form_edit.validate() and request.method == "POST":
        db.session.query(
            Product
        ).filter(Product.product_id == form_edit.product_id.data
        ).update({"name": (form_edit.name.data),"description": (form_edit.description.data),"price": (form_edit.price.data),"qty_available": (form_edit.qty_available.data)})
        db.session.commit()
    
    return render_template('farmerorderconfirm.html', products=products, form=form, form_edit=form_edit)

@other_blueprint.route('/confirmarrived', methods=['GET','POST'])
@login_required
def confirmarrived():
    if current_user.role != 'M':
        return redirect(url_for('other.index'))

    res = request.get_json()
    for item in res:
        try:
            prod_id = item["product_id"].split("_")[1]
            prod = db.session.query(
                Product
            ).filter(
                Product.product_id == prod_id
            ).one()
            prod.qty_warehoused = item["qty"]
            pio = db.session.query(
                ProductInOrder
            ).filter(
                ProductInOrder.product_id == prod_id
            ).all()
            for elem in pio:
                elem.confirmed = 2
        except Exception as e:
            print(e)
        db.session.commit()
    
    orders = db.session.query(
        Order
    ).filter(
        Order.status == "CONFIRMED"
    ).all()
    for elem in orders:
        # order_confs = db.session.query(
        #     Order,Product,ProductInOrder
        # ).filter(
        #     ProductInOrder.order_id == Order.order_id
        # ).filter(
        #     ProductInOrder.product_id == Product.product_id
        # ).filter(
        #     Order.order_id == elem.order_id
        # ).all()
        # print(order)
        # if len(order_confs) == 0:
        user = db.session.query(User).filter(User.id == elem.client_id).one()
        elem.status = "WAREHOUSED"
        subject = "Order Warehoused"
        msg = "Dear User, the order you submitted with id: #"+str(elem.order_id)+", with a total of €"+str(elem.total)+" has been Warehoused,\nIt will be prepared by one of our workers and brought to you according to the delivery date you have chosen.\nThanks, \nSPG Team."
        mail_sender(subject,msg,user.email)
            
    db.session.commit()
    return redirect(url_for('other.confirmarrivals'))

@other_blueprint.route('/getdate', methods=['GET'])
def getdate():
    date = session.get('date')
    return jsonify(date=date)

@other_blueprint.route('/updatedatetime', methods=['GET','POST'])
@login_required
def updatedatetime():
    new_date = request.get_json()
    print(new_date)
    session["date"] = new_date
    set_session_vars()
    return redirect(url_for('other.index'))

def set_session_vars():
    date, time = session["date"].split()
    day, month, year = list(map(int,date.split("-")))
    hour, minutes = list(map(int,time.split(":")))

    ans = datetime.date(year, month, day)
    session["weekday"] = ans.strftime("%A")
    week = ans.isoweekday() # days 1 .. 7

    session["place_order"] = False
    if (week == 6 and hour >= 9) or (week == 7 and hour < 23):
        session["place_order"] = True

    session["report_avail"] = False
    if (week == 3 and hour >= 9) or (week in range(4,6)) or (week == 6 and hour < 9):
        session["report_avail"] = True

    session["confirm_avail"] = False
    if (week == 7 and hour >= 23) or (week == 1 and hour < 9):
        session["confirm_avail"] = True

    session["farmer_delivery"] = False
    if (week == 1 and hour >= 9) or (week == 2 and hour < 23):
        session["farmer_delivery"] = True
    
    session["client_pickups"] = False
    if (week == 3 and hour >= 9) or (week == 4) or (week == 5 and hour < 23):
        session["client_pickups"] = True

    # wipe client carts
    if not session["place_order"]:
        ProductInBasket.query.delete()
        db.session.commit()

    # cancel orders with pending cancellation past deadline
    orders_pending_cancel = db.session.query(Order).filter(Order.status == "PENDING CANCELLATION").all()
    for order in orders_pending_cancel:
        order_date, order_time = order.order_date.split()
        order_day, order_month, order_year = list(map(int,order_date.split("-")))
        d = datetime.date(order_year, order_month, order_day)
        next_monday = next_weekday(d, 0) # 0 = Monday
        current= datetime.datetime.strptime(session["date"], "%d-%m-%Y %H:%M").date()
        
        if current > next_monday:
            order.status = "CANCELLED"
        db.session.commit()

    # confirm 0 avail if past confirmation deadline
    prod_pending_confirm = db.session.query(
            Order, ProductInOrder
        ).filter(
            Order.order_id == ProductInOrder.order_id
        ).filter(
            ProductInOrder.confirmed == 0
        ).all()

    for order, prod in prod_pending_confirm:
        order_date= datetime.datetime.strptime(order.order_date, "%d-%m-%Y %H:%M").date()
        current= datetime.datetime.strptime(session["date"], "%d-%m-%Y %H:%M").date()

        if not (session["confirm_avail"] or session["place_order"]) and current > order_date and order.status == "PENDING":
            confirm_order(order.order_id,prod.pio_id,prod.product_id,0)


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

@other_blueprint.route('/emptycart', methods=['GET','POST'])
@login_required
def emptycart():
    if current_user.role != 'C' and current_user.role != 'S':
        return redirect(url_for('other.index'))
    ProductInBasket.query.filter(ProductInBasket.client_id == current_user.id).delete()
    print("DElETING CART")
    db.session.commit() 
    session["cart_count"] = 0
    return redirect(url_for('other.shoppingcart'))

@other_blueprint.route('/updateorder', methods=['GET','POST'])
@login_required
def updateorder():
    if current_user.role != 'C':
        return redirect(url_for('other.index'))

    res = request.get_json()
    order = db.session.query(Order).filter(Order.order_id == res["order"]).one()
    products = db.session.query(ProductInOrder).filter(ProductInOrder.order_id == res["order"]).all()
    print(products[0].product_id)
    new_total = 0
    if order.home_delivery == 'F':
        new_total += 7.50
    print(res["values"])
    for item in res["values"]:
        item_id = item["product_id"].split("_")[1]
        print(item_id)
        for product in products:
            if product.product_id == int(item_id):
                print("UPDATE")
                product.quantity = item["qty"]
                prod = db.session.query(Product).filter(Product.product_id == item_id).one()
                new_total += float(item["qty"]) * prod.price

    order.total = new_total
    q2 = db.session.query(
        User
        ).filter(
            User.id == order.client_id
        ).filter(
            User.role == "C"
        ).first()
    balance = True
    if new_total > q2.wallet - q2.pending_amount:
        balance = False
        order.status = "PENDING CANCELLATION"
    else:
        order.status = "PENDING"
    # if not balance:
    #     # Send an email to the user to remind to top-up the wallet
    #     subject = "Insufficient Balance Reminder"
    #     msg = "Dear User, your balance is €" + str(round(q2.wallet-q2.pending_amount,2)) + " and is not sufficient to complete the order #"+str(order.order_id)+" with a total of €"+str(order.total)+",\nPlease make sure to charge your wallet. Thanks, \nSPG Team."
    #     mail_sender(subject,msg,q2.email)
    db.session.commit()


    return redirect(url_for('other.clientorders'))

################## AUTOCOMPLETE ROUTES ##############################
# @app.route('/autocomplete', methods=['GET'])
# def autocomplete():
#     search = request.args.get('q')
#     results = getComplete(search,session['env'])
#     return jsonify(matching_results=results)

@other_blueprint.route('/autocompletemail', methods=['GET','POST'])
@login_required
def autocompletemail():
    search = request.args.get('q')
    mails = db.session.query(User).from_statement(text("""select * from users
    where email like '%""" + str(search) + """%' and role = 'C' """)).all()
    results = []
    for mail in mails:
        results.append(mail.email)

    return jsonify(matching_results=results)
    # return "pogu"