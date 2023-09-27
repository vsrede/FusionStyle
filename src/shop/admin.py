from django.contrib import admin

from shop.models import Brand, Cart, Category, Favorite, Order, Product

admin.site.register([Product, Category, Brand, Order, Cart, Favorite])
