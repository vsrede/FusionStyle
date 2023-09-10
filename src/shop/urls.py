from django.urls import path

from shop.views import (AddToCartView, CartView, CreateOrderView, ProductDetailView,
                        ProductListView, RemoveFromCartView, UpdateCartView)

app_name = "shop"

urlpatterns = [
    path("products/<str:category>/", ProductListView.as_view(), name="products_list"),
    path("products", ProductListView.as_view(), name="products_list"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("add-to-cart/<int:product_id>/", AddToCartView.as_view(), name="add_to_cart"),
    path("cart/", CartView.as_view(), name="cart"),
    path("update-cart/<int:product_id>/", UpdateCartView.as_view(), name="update-cart"),
    path("remove-from-cart/<int:product_id>/", RemoveFromCartView.as_view(), name="remove-from-cart"),
    path("create-order", CreateOrderView.as_view(), name="create_order"),
]
