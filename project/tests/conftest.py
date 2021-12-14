from werkzeug.security import generate_password_hash
import pytest
from project import create_app, db
from project.models import User, Product, Order, ProductInOrder, ProductInBasket

@pytest.fixture(scope='module')
def new_user():
    user = User(name='Pat', surname='kennedy', email='patkennedy79@gmail.com', password='FlaskIsAwesome', role='S')
    return user

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!

@pytest.fixture(scope='module')
def init_database(test_client):
    db.create_all()

    # Insert User data
    user1 = User(name='Pat', surname='Farmer', email='patfarmer@gmail.com', role='F', password=generate_password_hash('FlaskIsAwesome', method='sha256'), company="Pat's Farm", pending_amount=0.0)
    user2 = User(name='Matt', surname='Smith', email='mattsmith@gmail.com', role='S', password=generate_password_hash('UserPassword', method='sha256'), company="", pending_amount=0.0)
    user3 = User(name='Ella', surname='Clint', email='ellaclint@gmail.com', role='C', password=generate_password_hash('UserPassword', method='sha256'), wallet=30, pending_amount=0.0)
    user4 = User(name='Ema', surname='Gow ', email='emagow@gmail.com', role='C', password=generate_password_hash('UserPassword', method='sha256'), wallet=10, pending_amount=0.0)
    user5 = User(name='John', surname='Doe', email='johndoe@gmail.com', role='W', password=generate_password_hash('UserPassword', method='sha256'), company="", pending_amount=0.0)
    user6 = User(name='Paul', surname='Right', email='paulright@gmail.com', role='M', password=generate_password_hash('UserPassword', method='sha256'), company="", pending_amount=0.0)

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)
    db.session.add(user6)
    db.session.commit()

    # Insert Product data
    prod1 = Product(name="Bananas", price=1, description="Bananas from Ecuador", qty_available=14, qty_requested=2, farmer_id=1, img_url="https://www.kroger.com/product/images/xlarge/front/0000000004011", date="2021-11-24")
    prod2 = Product(name="Potatoes", price=4, description="The best potatoes", qty_available=11, qty_requested=0, farmer_id=1, img_url="", date="2021-11-24")
    db.session.add(prod1)
    db.session.add(prod2)
    db.session.commit()

    # Insert Order data
    order1 = Order(client_id=3, delivery_address="Store", home_delivery="N", total=12, requested_delivery_date="2021-12-23", actual_delivery_date="2021-12-23", status="LODGED", order_date="2021-12-12")
    order2 = Order(client_id=3, delivery_address="This Street", home_delivery="Y", total=15, requested_delivery_date="2021-12-23", actual_delivery_date="2021-12-23", status="PENDING", order_date="2021-12-12")
    order3 = Order(client_id=4, delivery_address="That Street", home_delivery="Y", total=15, requested_delivery_date="2021-12-23", actual_delivery_date="2021-12-23", status="PREPARED", order_date="2021-12-12")
    order4 = Order(client_id=4, delivery_address="Store", home_delivery="N", total=15, requested_delivery_date="2021-12-23", actual_delivery_date="2021-12-23", status="PREPARED", order_date="2021-12-12")
    db.session.add(order1)
    db.session.add(order2)
    db.session.add(order3)
    db.session.add(order4)

    prod_in_order1 = ProductInOrder(product_id=1, order_id=1, quantity=2, confirmed=0)
    prod_in_order2 = ProductInOrder(product_id=1, order_id=2, quantity=2, confirmed=0)
    prod_in_order3 = ProductInOrder(product_id=2, order_id=2, quantity=2, confirmed=0)
    db.session.add(prod_in_order1)
    db.session.add(prod_in_order2)
    db.session.add(prod_in_order3)

    prod_in_bask1 = ProductInBasket(product_id=1, client_id=3, quantity=1)
    db.session.add(prod_in_bask1)

    db.session.commit()

    yield

    db.drop_all()

@pytest.fixture(scope='function')
def login_farmer_user(test_client):
    test_client.post('/login',
                     data=dict(email='patfarmer@gmail.com', password='FlaskIsAwesome'),
                     follow_redirects=True)

    yield

    test_client.get('/logout', follow_redirects=True)

@pytest.fixture(scope='function')
def login_employee_user(test_client):
    test_client.post('/login',
                     data=dict(email='mattsmith@gmail.com', password='UserPassword'),
                     follow_redirects=True)

    yield

    test_client.get('/logout', follow_redirects=True)

@pytest.fixture(scope='function')
def login_client_user(test_client):
    test_client.post('/login',
                     data=dict(email='ellaclint@gmail.com', password='UserPassword'),
                     follow_redirects=True)

    yield

    test_client.get('/logout', follow_redirects=True)

@pytest.fixture(scope='function')
def login_warehouse_employee_user(test_client):
    test_client.post('/login',
                     data=dict(email='johndoe@gmail.com', password='UserPassword'),
                     follow_redirects=True)

    yield

    test_client.get('/logout', follow_redirects=True)

@pytest.fixture(scope='function')
def login_warehouse_manager_user(test_client):
    test_client.post('/login',
                     data=dict(email='paulright@gmail.com', password='UserPassword'),
                     follow_redirects=True)

    yield

    test_client.get('/logout', follow_redirects=True)
