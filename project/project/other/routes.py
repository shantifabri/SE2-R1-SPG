from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from project.models import User, Product, Client, ProductRequest
from project.forms import ProductRequestForm, ClientInsertForm
from project import db

from . import other_blueprint

#### routes ####

@other_blueprint.route('/products')
@login_required
def products():
    if current_user.role != 'S':
        return redirect(url_for('index'))
    products = Product.query.all()
    return render_template('products.html',products=products)

@other_blueprint.route('/singleproduct/<product_id>',  methods=['GET','POST'])
@login_required
def singleproduct(product_id):
    if current_user.role != 'S':
        return redirect(url_for('index'))
    time = "ZZZZ:ZZZZ:ZZ:ZZ zz ZZ"
    form = ProductRequestForm()
    product = Product.query.filter_by(product_id=product_id).all()[0]
    if form.validate_on_submit():
        try:
            # print("INSERTING: " + product.name)
            # print(form.email.data)
            user = Client.query.filter_by(email=form.email.data).all()[0]
            productReq = ProductRequest(product_id=product.product_id, client_id=user.client_id, shop_id=current_user.id, quantity=form.quantity.data, timestamp=time)
            db.session.add(productReq)
            db.session.commit()
            return redirect(url_for('products'))
        except Exception as e:
            print(e)
            return render_template('singleproduct.html', product=product, form=form, valid=False)
    return render_template('singleproduct.html', product=product, form=form, valid=True)

@other_blueprint.route('/insertclient')
@login_required
def insertclient():
    if current_user.role != 'S':
        return redirect(url_for('index'))
    # name, surname, email, phone, wallet
    time = "ZZZZ:ZZZZ:ZZ:ZZ zz ZZ"
    form = ClientInsertForm()
    if form.validate_on_submit():
        productReq = ProductRequest(product_id=form.productId.data, client_id=form.client_id.data, shop_id=form.shop_id.data, quantity=form.quantity.data, timestamp=time)
        db.session.add(productReq)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('insertclient.html', form=form)