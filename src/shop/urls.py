from django.urls import path

from shop.views import ProductDetailView, ProductListView

app_name = "shop"

urlpatterns = [
    path("products/<str:category>/", ProductListView.as_view(), name="products_list"),
    path("products", ProductListView.as_view(), name="products_list"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]
