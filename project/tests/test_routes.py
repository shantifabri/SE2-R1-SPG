def test_home_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET) and no user is logged
    THEN check that the response is valid and shows correct options
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

def test_home_page_logged_as_employee(test_client, init_database, login_employee_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/home' page is requested (GET) and employee is logged in
    THEN check that the response is valid and shows the correct options
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Products" in response.data
    assert b"Manage Clients" in response.data
    assert b"Manage Orders" in response.data
    assert b"My Products" not in response.data
    assert b"Welcome" in response.data
    assert b"Log Out" in response.data
    assert b"Log In" not in response.data
    assert b"Sign Up" not in response.data

def test_home_page_logged_as_farmer(test_client, init_database, login_farmer_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/home' page is requested (GET) and farmer is logged in
    THEN check that the response is valid and shows the correct options
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Products" in response.data
    assert b"My Products" in response.data
    assert b"Manage Orders" in response.data
    assert b"Manage Clients" not in response.data
    assert b"Welcome" in response.data
    assert b"Log Out" in response.data
    assert b"Log In" not in response.data
    assert b"Sign Up" not in response.data

def test_home_page_logged_as_client(test_client, init_database, login_client_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/home' page is requested (GET) and client is logged in
    THEN check that the response is valid and shows the correct options
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Products" in response.data
    assert b"My Orders" in response.data
    assert b"Profile" in response.data
    assert b"My Products" not in response.data
    assert b"Manage Clients" not in response.data
    assert b"Manage Orders" not in response.data
    assert b"Welcome" in response.data
    assert b"Log Out" in response.data
    assert b"Log In" not in response.data
    assert b"Sign Up" not in response.data

def test_home_page_logged_as_warehouse_employee(test_client, init_database, login_warehouse_employee_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/home' page is requested (GET) and warehouse employee is logged in
    THEN check that the response is valid and shows the correct options
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Orders" in response.data
    assert b"My Orders" not in response.data
    assert b"Profile" not in response.data
    assert b"My Products" not in response.data
    assert b"Manage Clients" not in response.data
    assert b"Manage Orders" not in response.data
    assert b"Welcome" in response.data
    assert b"Log Out" in response.data
    assert b"Log In" not in response.data
    assert b"Sign Up" not in response.data

def test_home_page_logged_as_warehouse_manager(test_client, init_database, login_warehouse_manager_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/home' page is requested (GET) and warehouse manager is logged in
    THEN check that the response is valid and shows the correct options
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Orders" in response.data
    assert b"My Orders" not in response.data
    assert b"Profile" not in response.data
    assert b"My Products" not in response.data
    assert b"Manage Clients" not in response.data
    assert b"Manage Orders" not in response.data
    assert b"Welcome" in response.data
    assert b"Log Out" in response.data
    assert b"Log In" not in response.data
    assert b"Sign Up" not in response.data

def test_products_page_logged(test_client, init_database, login_employee_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/products' page is requested (GET) and user is logged in
    THEN check that the response is valid
    """
    response = test_client.get('/products')
    assert response.status_code == 200
    assert b"Vegetables" in response.data
    assert b"Fruit" in response.data


def test_single_product_page_logged(test_client, init_database, login_employee_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/products' page is requested (GET) and user is logged in
    THEN check that the response is valid
    """
    response = test_client.get('/singleproduct/1')
    assert response.status_code == 200
    assert b"Farmer" in response.data
    assert b"Description" in response.data
    assert b"Quantity" in response.data
    assert b"Add to Cart" in response.data

