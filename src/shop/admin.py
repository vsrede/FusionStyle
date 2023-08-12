from django.contrib import admin

from shop.models import Brand, Cart, Category, Order, Product

admin.site.register([Product, Category, Brand, Order, Cart])
