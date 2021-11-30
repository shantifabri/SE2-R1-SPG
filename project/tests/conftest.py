from werkzeug.security import generate_password_hash
import pytest
from project import create_app, db
from project.models import User, Product


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
    user1 = User(name='Pat', surname='Farmer', email='patfarmer@gmail.com', role='F', password=generate_password_hash('FlaskIsAwesome', method='sha256'), company="Pat's Farm")
    user2 = User(name='Matt', surname='Smith', email='mattsmith@gmail.com', role='S', password=generate_password_hash('UserPassword', method='sha256'), company="")
    user3 = User(name='Ella', surname='Clint', email='ellaclint@gmail.com', role='C', password=generate_password_hash('UserPassword', method='sha256'), wallet=30)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()

    # Insert Product data
    prod1 = Product(name="Bananas", price=1, description="Bananas from Ecuador", qty_available=14, qty_requested=2, farmer_id=1, img_url="https://www.kroger.com/product/images/xlarge/front/0000000004011", date="2021-11-24")
    prod2 = Product(name="Potatoes", price=4, description="The best potatoes", qty_available=11, qty_requested=0, farmer_id=1, img_url="", date="2021-11-24")
    db.session.add(prod1)
    db.session.add(prod2)
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