from project.models import User, Product

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the name, surname, email, role and password fields are defined correctly
    """
    user = User(name='John', surname='Snow', email='johnsnow@gmail.com', role='Farmer', password='UserPassword')
    assert user.name == 'John'
    assert user.surname == 'Snow'
    assert user.email == 'johnsnow@gmail.com'
    assert user.role == 'Farmer'
    assert user.password == 'UserPassword'