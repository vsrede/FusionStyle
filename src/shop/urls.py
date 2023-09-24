# from django.urls import path
#
# from shop.views import (AddToCartView, CartView, CreateOrderView,
#                         OrderDetailListView, OrdersListView,
#                         ProductAllListView, ProductDetailView, ProductListView,
#                         RemoveFromCartView, UpdateCartView,
#                         generate_instances_view)
#
# app_name = "shop"
#
# urlpatterns = [
#     path("products/<str:category>/", ProductListView.as_view(), name="products_list"),
#     path("products_all", ProductAllListView.as_view(), name="products_list_all"),
#     path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
#     path("add-to-cart/<int:product_id>/", AddToCartView.as_view(), name="add_to_cart"),
#     path("cart/", CartView.as_view(), name="cart"),
#     path("update-cart/<int:product_id>/", UpdateCartView.as_view(), name="update-cart"),
#     path("remove-from-cart/<int:product_id>/", RemoveFromCartView.as_view(), name="remove-from-cart"),
#     path("create-order", CreateOrderView.as_view(), name="create_order"),
#     path("orders-list/<int:pk>/", OrdersListView.as_view(), name="orders-list"),
#     path("orders-detail-list/<int:order_id>/", OrderDetailListView.as_view(), name="orders-detail-list"),
#     path("generate-instances/", generate_instances_view, name="generate_instances"),
# ]
# ----------------------------------------------------------
#
from django.urls import path

from shop.views import (AddToCartView, CartView, CreateOrderView,
                        OrderDetailListView, OrdersListView,
                        ProductAllListView, ProductDetailView, ProductListView,
                        RemoveFromCartView, UpdateCartView,
                        generate_instances_view)

app_name = "shop"

urlpatterns = [
    path("products/<str:category>/", ProductListView.as_view(), name="products_list"),
    path("products_all", ProductAllListView.as_view(), name="products_list_all"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("add-to-cart/<int:product_id>/", AddToCartView.as_view(), name="add_to_cart"),
    path("cart/", CartView.as_view(), name="cart"),
    path("update-cart/<int:product_id>/", UpdateCartView.as_view(), name="update-cart"),
    path("remove-from-cart/<int:product_id>/", RemoveFromCartView.as_view(), name="remove-from-cart"),
    path("create-order", CreateOrderView.as_view(), name="create_order"),
    path("orders-list/<int:pk>/", OrdersListView.as_view(), name="orders-list"),
    path("orders-detail-list/<int:order_id>/", OrderDetailListView.as_view(), name="orders-detail-list"),
    path("generate-instances/", generate_instances_view, name="generate_instances"),
    path(
        "products_list/price_asc/",
        ProductAllListView.as_view(),
        {"sort_by": "price_asc"},
        name="products_list_price_asc",
    ),
    path(
        "products_list/price_desc/",
        ProductAllListView.as_view(),
        {"sort_by": "price_desc"},
        name="products_list_price_desc",
    ),
    path(
        "products_all_list/price_asc/",
        ProductAllListView.as_view(),
        {"sort_by": "price_asc"},
        name="products_list_all_price_asc",
    ),
    path(
        "products_all_list/price_desc/",
        ProductAllListView.as_view(),
        {"sort_by": "price_desc"},
        name="products_list_all_price_desc",
    ),
]
