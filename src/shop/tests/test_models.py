from django.test import TestCase

from shop.models import Brand, Cart, Category, Order, Product
from utils.samples import (sample_brand, sample_cart, sample_category,
                           sample_customer, sample_order, sample_product)


class TestShopModel(TestCase):
    def setUp(self):
        self.customer = sample_customer()
        self.product = sample_product()
        self.category = sample_category()
        self.brand = sample_brand()

    def tearDown(self):
        self.customer.delete()
        self.product.delete()
        self.category.delete()
        self.brand.delete()

    def test_category_creation(self):
        category = sample_category()
        self.assertTrue(isinstance(category, Category))

    def test_brand_creation(self):
        brand = sample_brand()
        self.assertTrue(isinstance(brand, Brand))

    def test_product_creation(self):
        category = sample_category()
        brand = sample_brand()
        product = sample_product(category=category, brand=brand)
        self.assertTrue(isinstance(product, Product))

    def test_product_creation_name(self):
        category = sample_category()
        brand = sample_brand()
        product = sample_product(category=category, brand=brand)
        self.assertEqual(
            str(product),
            f"{product.name}, title: {product.title},  description: {product.description}price: {product.price}",
        )

    def test_order_creation(self):
        customer = sample_customer()
        product = sample_product()
        order = sample_order(customer=customer, products=[product])
        self.assertTrue(isinstance(order, Order))

    def test_cart_creation(self):
        customer = sample_customer()
        product = sample_product()
        cart = sample_cart(customer=customer, products=[product])
        self.assertTrue(isinstance(cart, Cart))

    def test_cart_creation_count_items(self):
        customer = sample_customer()
        product = sample_product()
        cart = sample_cart(customer=customer, products=[product])
        self.assertEqual(cart.total_items(), 1)

    def test_cart_creation_count_price(self):
        customer = sample_customer()
        product = sample_product()
        cart = sample_cart(customer=customer, products=[product])
        self.assertEqual(cart.total_price(), product.price)
