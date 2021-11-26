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