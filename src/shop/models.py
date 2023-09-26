import random

from django.contrib.auth import get_user_model
from django.db import models
from django_countries.fields import CountryField
from faker import Faker

from account.models import Customer
from core.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to="static/shop/product/", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="category")
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE, related_name="brand")

    def __str__(self):
        return f"{self.name}, title: {self.title}, description: {self.description}, price: {self.price}"

    @classmethod
    def generate_instances(cls, count=10):
        faker = Faker()
        category_count = Category.objects.count()
        brand_count = Brand.objects.count()

        for _ in range(count):
            cls.objects.create(
                name=faker.word(),
                title=faker.sentence(),
                description=faker.paragraph(nb_sentences=2),
                price=random.randint(50, 10000),
                stock=random.randint(0, 100),
                category=Category.objects.all()[random.randint(0, category_count - 1)],
                brand=Brand.objects.all()[random.randint(0, brand_count - 1)],
            )


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    @classmethod
    def generate_instances(cls, count=10):
        faker = Faker()
        for _ in range(count):
            cls.objects.create(
                name=faker.word(),
                description=faker.paragraph(nb_sentences=1),
            )


class Brand(models.Model):
    name = models.CharField(max_length=100)
    country = CountryField(max_length=100)
    description = models.TextField(max_length=255)
    logo = models.ImageField(upload_to="shop/brand/", null=True, blank=True)

    def __str__(self):
        return f"{self.name}, country: {self.country}"

    @classmethod
    def generate_instances(cls, count=10):
        faker = Faker()
        for _ in range(count):
            cls.objects.create(
                name=faker.word(),
                country=faker.country_code(),
                description=faker.paragraph(nb_sentences=1),
            )


class Cart(models.Model):
    customer = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    guest_session_id = models.CharField(max_length=50, null=True, blank=True)
    products = models.ManyToManyField(Product, related_name="cart")

    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.cart_items.all())

    def total_items(self):
        return sum(item.quantity for item in self.cart_items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Order(BaseModel):
    class ORDER_STATUS(models.IntegerChoices):
        ORDER_IN_PROCESSING = 0, "Order is processing"
        PENDING = 1, "Pending"
        COMPLETED = 2, "Completed"

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=ORDER_STATUS.choices, default=ORDER_STATUS.ORDER_IN_PROCESSING)
    products = models.ManyToManyField(Product, related_name="order")
    delivery_address = models.TextField(max_length=100, null=True, blank=True)
    delivery_first_name = models.CharField(max_length=50, null=True, blank=True)
    delivery_last_name = models.CharField(max_length=50, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Order for {self.customer} - {self.get_status_display()}"


class GuestCart(models.Model):
    session_key = models.CharField(max_length=128, unique=True)
    products = models.ManyToManyField(Product, through="GuestCartItem")
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.CASCADE)


class GuestCartItem(models.Model):
    cart = models.ForeignKey(GuestCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
