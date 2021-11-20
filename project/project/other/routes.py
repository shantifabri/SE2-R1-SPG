from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from project.models import User, Product, Client, ProductRequest, ProductInOrder, ProductInBasket
from project.forms import ProductRequestForm, ClientInsertForm, AddToCartForm
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
    if current_user.role != 'S' and current_user.role != 'C':
        return redirect(url_for('index'))
    time = "ZZZZ:ZZZZ:ZZ:ZZ zz ZZ"
    form = AddToCartForm()
    product = Product.query.filter_by(product_id=product_id).all()[0]
    if form.validate_on_submit():
        try:
            productReq = ProductInBasket(product_id=product.product_id, client_id=current_user.id, quantity=form.quantity.data)
            db.session.add(productReq)
            db.session.commit()
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