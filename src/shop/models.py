from django.db import models
from django_countries.fields import CountryField

from account.models import Customer
from core.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to="shop/product/", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="products_category")
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE, related_name="products_brand")

    def __str__(self):
        return f"{self.name}, title: {self.title},  description: {self.description}" f"price: {self.price}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    country = CountryField()
    description = models.TextField(max_length=255)

    def __str__(self):
        return f"{self.name}, country: {self.country},  description: {self.description}"


class Order(BaseModel):
    class ORDER_STATUS(models.IntegerChoices):
        ORDER_IN_PROCESSING = 0, "Order is processing"
        PENDING = 1, "Pending"
        COMPLETED = 2, "Completed"

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=ORDER_STATUS.choices, default=ORDER_STATUS.ORDER_IN_PROCESSING)
    products = models.ManyToManyField(Product, related_name="orders_products")
    delivery_address = models.TextField(max_length=255, null=True, blank=True)

    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.products.all())

    def __str__(self):
        return f"Order for {self.customer} - {self.get_status_display()}"


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name="carts")

    def total_price(self):
        return sum(item.price for item in self.products.all())

    def total_items(self):
        return self.products.count()
