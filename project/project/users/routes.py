from flask import render_template, request, flash, redirect, url_for, session
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from project.forms import RegisterForm, LoginForm
from project.models import User, ProductInBasket
from project import db

from . import users_blueprint


########### LOGIN AND SIGNUP ROUTES ########################

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data ).first()
        if user:
            # compares the password hash in the db and the hash of the password typed in the form
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                status_counts = db.session.query(ProductInBasket.client_id, db.func.count(ProductInBasket.product_id).label('count_id')
                ).filter(ProductInBasket.client_id == current_user.id).group_by(ProductInBasket.pib_id
                ).all()
                session["cart_count"] = session["cart_count"] = len(status_counts)
                
                return redirect(url_for('index'))
        return render_template('login.html', form=form, valid=False)

    return render_template('login.html', form=form, valid=True)


@users_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        # add the user form input which is form.'field'.data into the column which is 'field'
        new_user = User(name=form.name.data, surname=form.surname.data, role=form.role.data, email=form.email.data, password=hashed_password, company=form.company.data, wallet=0)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))