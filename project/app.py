from flask import Flask, render_template, redirect, url_for, session
from flask_bootstrap import Bootstrap


from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegisterForm, ProductRequestForm, ClientInsertForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NOBODY-CAN-GUESS-THIS'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    email = db.Column(db.String(30), unique=True)
    role = db.Column(db.String(30))
    password = db.Column(db.String(80))

class ProductRequests(db.Model):
    productrequest_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    client_id = db.Column(db.Integer)
    shop_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    timestamp = db.Column(db.String(40))

class Clients(db.Model):
    client_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    wallet = db.Column(db.Float)

class Products(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    price = db.Column(db.Float)
    qty_available = db.Column(db.Integer)
    qty_requested = db.Column(db.Integer)
    farmer_id = db.Column(db.Integer)
    img_url = db.Column(db.String(50))


@login_manager.user_loader
def load_user(user_id):
    user = Users.query.get(int(user_id))
    # session["name"] = user.name
    # session["surname"] = user.surname
    # session["email"] = user.email
    # session["role"] = user.role
    session["logged"] = True
    return user



# Index Page used for landing.
@app.route('/')
def index():
    try:
        print(current_user.role)
        if current_user.role == "F":
            return render_template('index_farmer.html')
        elif current_user.role == "S":
            return render_template('index_shop.html')
        elif current_user.role == "A":
            return render_template('index_admin.html')
        else:
            return render_template('index.html')
    except:
        return render_template('index.html')

########### LOGIN AND SIGNUP ROUTES ########################

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data ).first()
        if user:
            # compares the password hash in the db and the hash of the password typed in the form
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))
        return 'invalid username or password'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        # add the user form input which is form.'field'.data into the column which is 'field'
        new_user = Users(name=form.name.data, surname=form.surname.data, role=form.role.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

########## FUNCTIONAL ROUTES ######################################

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/products')
@login_required
def products():
    products = Products.query.all()
    for prod in products:
        print(prod.name)

    return render_template('products.html',products=products)

@app.route('/productrequest')
@login_required
def productrequest():
    # product_id, client_id, shop_id, quantity, timestamp.
    time = "ZZZZ:ZZZZ:ZZ:ZZ zz ZZ"
    form = ProductRequestForm()
    if form.validate_on_submit():
        productReq = ProductRequests(product_id=form.product_id.data, client_id=form.client_id.data, shop_id=form.shop_id.data, quantity=form.quantity.data, timestamp=time)
        db.session.add(productReq)
        db.session.commit()
        return render_template('products.html')
    return render_template('productrequest.html', form=form)

@app.route('/insertclient')
@login_required
def insertclient():
    # name, surname, email, phone, wallet
    time = "ZZZZ:ZZZZ:ZZ:ZZ zz ZZ"
    form = ClientInsertForm()
    if form.validate_on_submit():
        productReq = ProductRequests(product_id=form.productId.data, client_id=form.client_id.data, shop_id=form.shop_id.data, quantity=form.quantity.data, timestamp=time)
        db.session.add(productReq)
        db.session.commit()
        return render_template('index.html')
    return render_template('productrequest.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)