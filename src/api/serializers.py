from django.contrib.auth import get_user_model
from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from shop.models import Brand, Order, Product


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "city", "is_staff", "email")


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "title", "description", "price", "category", "brand")


class OrderSerializer(ModelSerializer):
    status = CharField(source="get_status_display")
    customer = SerializerMethodField()
    products = SerializerMethodField()

    def get_customer(self, obj):
        return obj.customer.email

    def get_products(self, obj):
        return ", ".join([product.name for product in obj.products.all()])

    class Meta:
        model = Order
        fields = ("status", "delivery_address", "customer", "products")


class OrderCreateSerializer(OrderSerializer):
    def get_customer(self, obj):
        return self.context["request"].data.get("customer")

    def get_products(self, obj):
        return self.context["request"].data.get("products")


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ("name", "country", "description")
