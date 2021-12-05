from flask import render_template, request, flash, redirect, url_for, session
from flask_login import login_user, current_user, login_required, logout_user

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import func
from wtforms.fields import datetime
from sqlalchemy.sql import text
import os

from project.models import User, Product, Client, ProductRequest, ProductInOrder, ProductInBasket, Order
from project.forms import ProductRequestForm, ClientInsertForm, AddToCartForm, TopUpForm, CheckOutForm, TopUpSearch, ProductInsertForm, ProductEditForm, CheckOutClientForm
from project import db
import datetime

from . import other_blueprint

#### routes ####
@other_blueprint.route('/')
def index():
    return render_template('index.html')

@other_blueprint.route('/products')
@login_required
def products():
    if current_user.role != 'S' and current_user.role != 'C' and current_user.role != 'F':
        return redirect(url_for('other.index'))
    # products = Product.query.all()
    products = db.session.query(
        Product, 
        User
        ).filter(
            User.id == Product.farmer_id
        ).all()
    return render_template('products.html',products=products)

@other_blueprint.route('/singleproduct/<product_id>',  methods=['GET','POST'])
@login_required
def singleproduct(product_id):
    if current_user.role != 'S' and current_user.role != 'C' and current_user.role != 'F':
        return redirect(url_for('other.index'))
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
@login_required
def insertclient():
    if current_user.role != 'S':
        return redirect(url_for('other.index'))
    # name, surname, email, phone, wallet
    time = "ZZZZ:ZZZZ:ZZ:ZZ zz ZZ"
    form = ClientInsertForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        # add the user form input which is form.'field'.data into the column which is 'field'
        new_user = User(name=form.name.data, surname=form.surname.data, role='C', email=form.email.data, password=hashed_password, company="Client", wallet=0)
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

@other_blueprint.route('/updatestatus/<order_id>',  methods=['GET','POST'])
@login_required
def updatestatus(order_id):
    if current_user.role != 'S':
        return redirect(url_for('other.index'))

    order = db.session.query(Order).filter(Order.order_id == order_id).one()
    order.status = "DELIVERED"
    db.session.commit()

    return redirect(url_for('other.shoporders'))

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
        total += val[0].quantity * val[1].price
        products.append(prod)
    vals["subtotal"] = '%.2f' % total
    vals["products"] = products
    vals["total"] = '%.2f' % (total + float(session.get("shipping",0)))


    if request.method == "POST":
        print(form.email.data)
        print(form.delivery_address.data)
        print(form.date.data)

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
                    new_order = Order(client_id=q2.id, delivery_address=address, home_delivery=home_delivery, total=vals["total"], requested_delivery_date=session.get("date",datetime.datetime.now()), actual_delivery_date="", status="PENDING CANCELLATION")
                else:
                    new_order = Order(client_id=q2.id, delivery_address=address, home_delivery=home_delivery, total=vals["total"], requested_delivery_date=session.get("date",datetime.datetime.now()), actual_delivery_date="", status="PENDING")
                # When a new order is added, the amount must be added to the pending amount.
                db.session.add(new_order)
                db.session.commit()
                ProductInBasket.query.filter_by(client_id=current_user.id).delete()

                items = []
                for prod in products:
                    items.append(ProductInOrder(product_id=prod["product_id"], quantity=prod["quantity"], order_id=new_order.order_id, confirmed=False))
                db.session.bulk_save_objects(items)
                db.session.commit()
                status_counts = db.session.query(ProductInBasket.client_id, db.func.count(ProductInBasket.product_id).label('count_id')
                    ).filter(ProductInBasket.client_id == current_user.id).group_by(ProductInBasket.pib_id
                    ).all()
                session["cart_count"] = len(status_counts)

                if not balance:
                    # Send an email to the user to remind to top-up the wallet
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
        # print(form.email.data)
        db.session.query(
            User
        ).filter(User.email == form.email.data
        ).update({"wallet": (User.wallet + form.amount.data)})
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
    
    return render_template('manageproducts.html', products=products, form=form, form_edit=form_edit)

@other_blueprint.route('/farmerorders', methods=['GET', 'POST'])
@login_required
def farmerorders():
    if current_user.role != 'F':
        return redirect(url_for('other.index'))

    orders = db.session.query(Order,ProductInOrder,Product).from_statement(text('''select * from products join 
            (select * from orders o join product_in_order pio on o.order_id = pio.order_id)a
            on products.product_id = a.product_id
            where farmer_id = ''' + str(current_user.id) + ''' and STATUS = 'PENDING';''')).all()
    print(orders)
    return render_template('farmerorders.html', orders=orders)

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
        ).all()
    return render_template('managerorders.html', orders=orders)