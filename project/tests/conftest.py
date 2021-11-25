import pytest
from project import create_app, db
from project.models import User, Product

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
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(name='Pat', surname='Farmer', email='patfarmer@gmail.com', role='Farmer', password='FlaskIsAwesome', company="Pat's Farm")
    user2 = User(name='Matt', surname='Smith', email='mattsmith@gmail.com', role='Shop Manager', password='UserPassword', company="")
    user3 = User(name='Ella', surname='Clint', email='ellaclint@gmail.com', role='Client', password='UserPassword', wallet=30)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)


    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()

