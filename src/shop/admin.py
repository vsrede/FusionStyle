from django.contrib import admin
from shop.models import Product, Category, Brand, Order, Cart

admin.site.register([Product, Category, Brand, Order, Cart])
