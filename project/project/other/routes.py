from flask import render_template, request, flash, redirect, url_for, session
from flask_login import login_user, current_user, login_required, logout_user

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import func
from wtforms.fields import datetime
import os

from project.models import User, Product, Client, ProductRequest, ProductInOrder, ProductInBasket, Order
from project.forms import ProductRequestForm, ClientInsertForm, AddToCartForm, TopUpForm, CheckOutForm, TopUpSearch, ProductInsertForm
from project import db
import datetime

from . import other_blueprint

#### routes ####

@other_blueprint.route('/products')
@login_required
def products():
    if current_user.role != 'S' and current_user.role != 'C' and current_user.role != 'F':
        return redirect(url_for('index'))
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
        return redirect(url_for('index'))
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
        return redirect(url_for('index'))
    # name, surname, email, phone, wallet
    time = "ZZZZ:ZZZZ:ZZ:ZZ zz ZZ"
    form = ClientInsertForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        # add the user form input which is form.'field'.data into the column which is 'field'
        new_user = User(name=form.name.data, surname=form.surname.data, role='C', email=form.email.data, password=hashed_password, company="Client", wallet=0)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('insertclient.html', form=form)

@other_blueprint.route('/updatequantity/<pib_id>/<amount>',  methods=['GET','POST'])
@login_required
def updatequantity(pib_id,amount):
    if current_user.role != 'S' and current_user.role != 'C':
        return redirect(url_for('index'))
    amount = int(amount)
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
        return redirect(url_for('index'))

    if value == "home":
        session["shipping"] = '%.2f' % 7.50
    else:
        session["shipping"] = 0

    return redirect(url_for('other.shoppingcart'))

@other_blueprint.route('/shoppingcart', methods=['GET','POST'])
def shoppingcart():
    if current_user.role != 'S' and current_user.role != 'C':
        return redirect(url_for('index'))
    
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
            return render_template('shoppingcart.html', values=vals, form=form, valid=False, date=True)
        else:
            if session.get("shipping",0) == 0:
                address = "Store"
                home_delivery = "N"
            else:
                address = form.delivery_address.data
                home_delivery = "F"

            if address != None:
                new_order = Order(client_id=q2.id, delivery_address=address, home_delivery=home_delivery, total=vals["total"], requested_delivery_date=session.get("date",datetime.datetime.now()), actual_delivery_date="", status="PENDING")
                db.session.add(new_order)
                db.session.commit()
                ProductInBasket.query.filter_by(client_id=current_user.id).delete()

                items = []
                for prod in products:
                    items.append(ProductInOrder(product_id=prod["product_id"], quantity=prod["quantity"], order_id=new_order.order_id))
                db.session.bulk_save_objects(items)
                db.session.commit()
                status_counts = db.session.query(ProductInBasket.client_id, db.func.count(ProductInBasket.product_id).label('count_id')
                    ).filter(ProductInBasket.client_id == current_user.id).group_by(ProductInBasket.pib_id
                    ).all()
                session["cart_count"] = len(status_counts)
                return redirect(url_for('index'))
                
                # order_id = new_order.order_id


            
    return render_template('shoppingcart.html', values=vals, form=form, valid=True, date=True)

@other_blueprint.route('/manageclients', methods=['GET','POST'])
@login_required
def manageclients():
    if current_user.role != 'S':
        return redirect(url_for('index'))
    return render_template('manageclients.html')

@other_blueprint.route('/insertproducts', methods=['GET','POST'])
@login_required
def insertproducts():
    if current_user.role != 'F':
        return redirect(url_for('index'))
    return render_template('insertproduct.html')

@other_blueprint.route('/topup', methods=['GET','POST'])
@login_required
def topup():
    if current_user.role != 'S':
        return redirect(url_for('index'))
    form = TopUpForm()
    form_search = TopUpSearch()
    users = db.session.query(
        User
    ).filter(
        User.role == "C"
    ).all()
    if form_search.validate_on_submit:
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
def manageproducts():
    form = ProductInsertForm()
    products = db.session.query(
        Product
    ).filter(
        Product.farmer_id == current_user.id
    ).all()
    if form.validate_on_submit and request.method == "POST":

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
    return render_template('manageproducts.html', products=products, form=form)