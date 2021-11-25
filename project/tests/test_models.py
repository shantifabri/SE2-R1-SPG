from project.models import User, Product, ProductRequest, ProductInOrder, ProductInBasket, Order

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the name, surname, email, role, password and company fields are defined correctly
    """
    user = User(name='John', surname='Snow', email='johnsnow@gmail.com', role='F', password='UserPassword', company="That one farm")
    assert user.name == 'John'
    assert user.surname == 'Snow'
    assert user.email == 'johnsnow@gmail.com'
    assert user.role == 'F'
    assert user.password == 'UserPassword'
    assert user.company == "That one farm"

def test_new_client():
    """
    GIVEN a User model
    WHEN a new Client is created
    THEN check the name, surname, email, role, password and wallet fields are defined correctly
    """
    client = User(name='Will', surname='Gray', email='willgray@gmail.com', role='C', password='UserPassword', wallet=145)
    assert client.name == 'Will'
    assert client.surname == 'Gray'
    assert client.email == 'willgray@gmail.com'
    assert client.role == 'C'
    assert client.password == 'UserPassword'
    assert client.wallet == 145


def test_new_product():
    """
    GIVEN a Product model
    WHEN a new Product is created
    THEN check the name, price, qty_available, qty_requested, farmer_id and img_url fields are defined correctly
    """
    product = Product(name="Bananas", price=4, description="Bananas from Ecuador", qty_available=14, qty_requested=2, farmer_id=3, img_url="https://www.kroger.com/product/images/xlarge/front/0000000004011", date="2021-11-24")
    
    assert product.name == "Bananas"
    assert product.price == 4 
    assert product.description == "Bananas from Ecuador"
    assert product.qty_available == 14
    assert product.qty_requested == 2
    assert product.farmer_id == 3
    assert product.img_url == "https://www.kroger.com/product/images/xlarge/front/0000000004011"
    assert product.date == "2021-11-24"

def test_new_product_request():
    """
    GIVEN a ProductRequest model
    WHEN a new ProductRequest is created
    THEN check the product_id, client_id, shop_id, quantity and timestamp fields are defined correctly
    """
    product_request = ProductRequest(product_id=1, client_id=4, shop_id=3, quantity=2, timestamp='2021-08-14 20:45:23')

    assert product_request.product_id == 1
    assert product_request.client_id == 4
    assert product_request.shop_id == 3
    assert product_request.quantity == 2
    assert product_request.timestamp == '2021-08-14 20:45:23'

def test_new_product_in_order():
    """
    GIVEN a ProductInOrder model
    WHEN a new ProductInOrder is created
    THEN check the product_id, order_id and quantity fields are defined correctly
    """
    product_in_order = ProductInOrder(product_id=1, order_id=2, quantity=3)

    assert product_in_order.product_id == 1
    assert product_in_order.order_id == 2
    assert product_in_order.quantity == 3

def test_new_product_in_basket():
    """
    GIVEN a ProductInBasket model
    WHEN a new ProductInBasket is created
    THEN check the product_id, client_id and quantity fields are defined correctly
    """
    product_in_basket = ProductInBasket(product_id=1, client_id=4, quantity=3)

    assert product_in_basket.product_id == 1
    assert product_in_basket.client_id == 4
    assert product_in_basket.quantity == 3

def test_new_order():
    """
    GIVEN a Order model
    WHEN a new Order is created
    THEN check the client_id, delivery_address, home_delivery, total, requested_delivery_date, actual_delivery_date and status fields are defined correctly
    """
    order = Order(client_id=4, delivery_address="St Marc Road", home_delivery="F", total=23, requested_delivery_date="2021-11-28", actual_delivery_date="2021-11-29", status="ACCEPTED")

    assert order.client_id == 4
    assert order.delivery_address == "St Marc Road"
    assert order.home_delivery == "F"
    assert order.total == 23
    assert order.requested_delivery_date == "2021-11-28"
    assert order.actual_delivery_date == "2021-11-29"
    assert order.status == "ACCEPTED"
