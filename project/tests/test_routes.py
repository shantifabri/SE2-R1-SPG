from flask import url_for, request

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
    WHEN the '/' page is posted to (POST)
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
    assert b"Categories" in response.data
    assert b"Vegetables" in response.data
    assert b"Fruit" in response.data
    assert b'Bananas' in response.data

def test_products_page_not_logged_redirects(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/products' page is requested (GET) and user is not logged in
    THEN check that it gets redirected to login and the response is valid
    """
    response = test_client.get('/products', follow_redirects=True)
    assert response.status_code == 200
    assert b"Categories" not in response.data
    assert b"Please log in" in response.data

    assert request.path == url_for('users.login')

def test_products_page_unauthorized_logged_redirects(test_client, init_database, login_warehouse_employee_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/products' page is requested (GET) and user is logged in as unauthorized role
    THEN check that it gets redirected to index and the response is valid
    """
    response = test_client.get('/products', follow_redirects=True)
    assert response.status_code == 200
    assert b"Categories" not in response.data
    assert b"Order fresh and genuine products everyday" in response.data

    assert request.path == url_for('other.index')

def test_single_product_page_logged(test_client, init_database, login_employee_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/singleproduct/<id>' page is requested (GET) and user is logged in
    THEN check that the response is valid
    """
    response = test_client.get('/singleproduct/1')
    assert response.status_code == 200
    assert b"Farmer" in response.data
    assert b"Description" in response.data
    assert b"Quantity" in response.data
    assert b"Add to Cart" in response.data

def test_single_product_page_not_logged_redirects(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/singleproduct/<id>' page is requested (GET) and user is not logged in
    THEN check that it gets redirected to login and the response is valid
    """
    response = test_client.get('/singleproduct/1', follow_redirects=True)
    assert response.status_code == 200
    assert b"Farmer" not in response.data
    assert b"Add to Cart" not in response.data
    assert b"Please log in" in response.data

    assert request.path == url_for('users.login')

def test_single_product_page_unauthorized_logged_redirects(test_client, init_database, login_warehouse_employee_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/singleproduct/<id>' page is requested (GET) and user is logged in as unauthorized role
    THEN check that it gets redirected to index and the response is valid
    """
    response = test_client.get('/singleproduct/1', follow_redirects=True)
    assert response.status_code == 200
    assert b"Add to Cart" not in response.data
    assert b"Order fresh and genuine products everyday" in response.data

    assert request.path == url_for('other.index')

def test_single_product_page_post(test_client, init_database, login_employee_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/singleproduct/<id>' page is posted to (POST)
    THEN check that it gets redirected to products after post and the response is valid
    """
    response = test_client.post('/singleproduct/1',
                                data=dict(quantity=2),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Categories" in response.data

### Shop Employee Routes ###
def test_manage_clients_page_logged_employee(test_client, init_database, login_employee_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/manageclients' page is requested (GET) and employee is logged in
    THEN check that the response is valid
    """
    response = test_client.get('/manageclients')
    assert response.status_code == 200
    assert b"Add a new Client" in response.data
    assert b"Top-up a wallet" in response.data

def test_manage_clients_page_not_logged(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/manageclients' page is requested (GET) and user is not logged in
    THEN check that it redirects to login and the response is valid
    """
    response = test_client.get('/manageclients', follow_redirects=True)
    assert response.status_code == 200
    assert b"Add a new Client" not in response.data
    assert b"Top-up a wallet" not in response.data
    assert b"Please log in" in response.data

    assert request.path == url_for('users.login')

def test_manage_clients_page_unauthorized_logged(test_client, init_database, login_farmer_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/manageclients' page is requested (GET) and user is logged as unauthorized role
    THEN check that it redirects to index and the response is valid
    """
    response = test_client.get('/manageclients', follow_redirects=True)
    assert response.status_code == 200
    assert b"Add a new Client" not in response.data
    assert b"Top-up a wallet" not in response.data

    assert request.path == url_for('other.index')

def test_insert_clients_page_logged_employee(test_client, init_database, login_employee_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/insertclient' page is requested (GET) and user is logged as employee
    THEN check that the response is valid
    """
    response = test_client.get('/insertclient')
    assert response.status_code == 200
    assert b"Insert a new Client" in response.data
    assert b"Name" in response.data

def test_insert_clients_page_unauthorized_logged(test_client, init_database, login_farmer_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/insertclient' page is requested (GET) and user is logged as unauthorized role
    THEN check that it redirects to index and the response is valid
    """
    response = test_client.get('/insertclient',  follow_redirects=True)
    assert response.status_code == 200
    assert b"Insert a new Client" not in response.data

    assert request.path == url_for('other.index')

def test_insert_clients_page_post_logged_employee(test_client, init_database, login_employee_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/insertclient' page is posted to (POST) and user is logged as employee
    THEN check that the response is valid and redirects to index
    """
    response = test_client.post('/insertclient',
                                data=dict(name='Donald', surname='Johnson', email='donaldjohnson@yahoo.com', password='FlaskIsGreat'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Manage Clients" in response.data

    assert request.path == url_for('other.index')

def test_topup_page_logged_employee(test_client, init_database, login_employee_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/topup' page is requested (GET) and user is logged as employee
    THEN check that the response is valid
    """
    response = test_client.get('/topup')
    assert response.status_code == 200
    assert b"Wallets Top-Up" in response.data
    assert b"Clients" in response.data
    assert b"Please, select the customer you want to top up for" in response.data
    assert b"ellaclint@gmail.com" in response.data
    assert b"emagow@gmail.com" in response.data
    assert b"30.00" in response.data #client's initial value
    
def test_topup_page_unauthorized_logged(test_client, init_database, login_farmer_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/topup' page is requested (GET) and user is logged as unauthorized role
    THEN check that it redirects to index and the response is valid
    """
    response = test_client.get('/topup',  follow_redirects=True)
    assert response.status_code == 200
    assert b"Wallets Top-Up" not in response.data

    assert request.path == url_for('other.index')

def test_topup_page_search_post_logged_employee(test_client, init_database, login_employee_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/topup' page is posted to as search (POST) and user is logged as employee
    THEN check that the response is valid and searches correctly
    """
    response = test_client.post('/topup',
                                data=dict(search='ella'))
    assert response.status_code == 200
    assert b"ellaclint@gmail.com" in response.data
    assert b"emagow@gmail.com" not in response.data

def test_topup_page_wallet_post_logged_employee(test_client, init_database, login_employee_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/topup' page is posted to as wallet amount (POST) and user is logged as employee
    THEN check that the response is valid and wallet updates correctly
    """
    response = test_client.post('/topup',
                                data=dict(email='ellaclint@gmail.com', amount=2))
    assert response.status_code == 200
    assert b"ellaclint@gmail.com" in response.data
    assert b"emagow@gmail.com" in response.data
    assert b"32.00" in response.data #client's updated value
    assert b"30.00" not in response.data #client's initial value

def test_shop_orders_page_logged_employee(test_client, init_database, login_employee_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/shoporders' page is requested (GET) and user is logged as employee
    THEN check that the response is valid
    """
    response = test_client.get('/shoporders')
    assert response.status_code == 200
    assert b"Orders handout" in response.data
    assert b"Please, select the order you want to hand out" in response.data
    assert b"Hand Out" in response.data
    assert b"DELIVERED" not in response.data

def test_shop_orders_page_unauthorized_logged(test_client, init_database, login_farmer_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/shoporders' page is requested (GET) and user is logged as unauthorized role
    THEN check that it redirects to index and the response is valid
    """
    response = test_client.get('/shoporders',  follow_redirects=True)
    assert response.status_code == 200
    assert b"Orders handout" not in response.data

    assert request.path == url_for('other.index')

def test_update_status_logged_employee(test_client, init_database, login_employee_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/updatestatus/<order_id>' page is posted to (POST) and user is logged as employee
    THEN check that the response is valid, it updates order status and redirects to orders
    """
    response = test_client.post('/updatestatus/1',  follow_redirects=True)
    assert response.status_code == 200
    assert b"Hand Out" not in response.data
    assert b"DELIVERED" in response.data

    assert request.path == url_for('other.shoporders')

def test_update_status_unauthorized_logged(test_client, init_database, login_farmer_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/updatestatus/<order_id>' page is posted to (POST) and user is logged as unauthorized role
    THEN check that it redirects to index and the response is valid
    """
    response = test_client.post('/updatestatus/1',  follow_redirects=True)
    assert response.status_code == 200
    assert b"Orders handout" not in response.data

    assert request.path == url_for('other.index')

### Farmer Routes ###
def test_manage_products_page_logged_farmer(test_client, init_database, login_farmer_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/manageproducts' page is requested (GET) and user is logged as farmer
    THEN check that the response is valid
    """
    pass
    # response = test_client.get('/manageproducts')
    # assert response.status_code == 200
    # assert b"Manage Products" in response.data

def test_manage_products_page_unauthorized_logged(test_client, init_database, login_employee_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/manageproducts' page is requested (GET) and user is logged as unauthorized role
    THEN check that it redirects to index and the response is valid
    """
    response = test_client.get('/manageproducts',  follow_redirects=True)
    assert response.status_code == 200
    assert b"Manage Products" not in response.data

    assert request.path == url_for('other.index')

def test_manage_products_post_new_logged_farmer(test_client, init_database, login_farmer_user):
    pass

def test_manage_products_post_edit_logged_farmer(test_client, init_database, login_farmer_user):
    pass

def test_farmer_orders_page_logged_farmer(test_client, init_database, login_farmer_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/farmerorders' page is requested (GET) and user is logged as farmer
    THEN check that the response is valid
    """
    response = test_client.get('/farmerorders')
    assert response.status_code == 200
    assert b"Orders Confirmation" in response.data
    assert b"Please, select the orders you want to confirm" in response.data
    assert b"This Street" in response.data
    assert b"15.00" in response.data

def test_farmer_orders_page_unauthorized_logged(test_client, init_database, login_employee_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/farmerorders' page is requested (GET) and user is logged as unauthorized role
    THEN check that it redirects to index and the response is valid
    """
    response = test_client.get('/farmerorders',  follow_redirects=True)
    assert response.status_code == 200
    assert b"Orders Confirmation" not in response.data

    assert request.path == url_for('other.index')

### Client Routes ###
def test_client_orders_page_logged_client(test_client, init_database, login_client_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/clientorders' page is requested (GET) and user is logged as client
    THEN check that the response is valid
    """
    response = test_client.get('/clientorders')
    assert response.status_code == 200
    assert b"Check your Orders" in response.data
    assert b"You can change quantities, delivery address and delivery date" in response.data
    assert b"12.00" in response.data

def test_client_orders_page_unauthorized_logged(test_client, init_database, login_farmer_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/clientorders' page is requested (GET) and user is logged as unauthorized role
    THEN check that it redirects to index and the response is valid
    """
    response = test_client.get('/clientorders',  follow_redirects=True)
    assert response.status_code == 200
    assert b"Check your Orders" not in response.data

    assert request.path == url_for('other.index')

### ###
def test():
    pass