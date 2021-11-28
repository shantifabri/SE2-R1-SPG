def test_home_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Oner SPG" in response.data
    assert b"Order fresh and genuine products everyday" in response.data
    assert b"Log In" in response.data
    assert b"Sign Up" in response.data
    assert b"Log Out" not in response.data

def test_home_page_post(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client.post('/')
    assert response.status_code == 405
    assert b"Order fresh and genuine products everyday" not in response.data
