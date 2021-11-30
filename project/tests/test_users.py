def test_login_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'log in' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data

def test_signup_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signup' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/signup')
    assert response.status_code == 200
    assert b'Sign Up' in response.data
    assert b'Name' in response.data
    assert b'Surname' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data
    assert b'Role' in response.data

def test_valid_login_logout(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                     data={'email': 'mattsmith@gmail.com', 'password': 'UserPassword'},
                     follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid Credentials. Please try Again..' not in response.data
    assert b'Log Out' in response.data
    assert b'Log In' not in response.data
    assert b'Sign Up' not in response.data

    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Logout' not in response.data
    assert b'Log In' in response.data
    assert b'Sign Up' in response.data

def test_invalid_login(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to with invalid credentials (POST)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/login',
                                data=dict(email='mattsmith@gmail.com', password='FlaskIsNotAwesome'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid Credentials. Please try Again..' in response.data
    assert b'Please log in' in response.data
    assert b'Sign in' in response.data
    assert b'Logout' not in response.data
    assert b'Log In' in response.data
    assert b'Sign Up' in response.data

def test_valid_signup(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signup' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/signup',
                                data=dict(name='Chris', surname='Johnson', company='CJ company', email='chrisjohnson@yahoo.com', password='FlaskIsGreat', role="F"),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Log Out' not in response.data
    assert b'Name' not in response.data
    assert b'Email' not in response.data
    assert b'Log In' in response.data


def test_invalid_signup(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signup' page is posted to (POST)
    THEN check the response is invalid
    """
    response = test_client.post('/signup',
                                data=dict(name='Chris', surname='Johnson',company='CJ company', email='chrisjohnson', password='FlaskIsGreat'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid Email' in response.data
    assert b'Log In' in response.data
    assert b'Sign Up' in response.data


