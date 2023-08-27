import uuid

from account.models import Customer
from shop.models import Brand, Cart, Category, Order, Product


def sample_category(name="Sample Category", description="Sample Category Description"):
    return Category.objects.create(name=name, description=description)


def sample_brand(name="Sample Brand", country="USA", description="Sample Brand Description"):
    return Brand.objects.create(name=name, country=country, description=description)


def sample_product(
    name="Sample Product",
    title="Sample Product Title",
    description="Sample Product Description",
    price=10.0,
    stock=100,
    category=None,
    brand=None,
):
    if category is None:
        category = sample_category()
    if brand is None:
        brand = sample_brand()

    return Product.objects.create(
        name=name, description=description, title=title, price=price, stock=stock, category=category, brand=brand
    )


def sample_customer(email=None, password="11111111"):
    if email is None:
        email = f"{uuid.uuid4()}@example.com"
    return Customer.objects.create_user(email=email, password=password)


def sample_order(customer=None, status=Order.ORDER_STATUS.ORDER_IN_PROCESSING, products=None, delivery_address=None):
    if customer is None:
        customer = sample_customer()

    if products is None:
        products = [sample_product()]

    order = Order.objects.create(customer=customer, status=status, delivery_address=delivery_address)
    order.products.set(products)
    return order


def sample_cart(customer=None, products=None):
    if customer is None:
        customer = sample_customer()

    if products is None:
        products = [sample_product(brand=sample_brand())]

    cart = Cart.objects.create(customer=customer)
    cart.products.set(products)
    return cart
