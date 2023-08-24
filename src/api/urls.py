from django.conf.urls import include
from django.urls import path
from drf_yasg import openapi
from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from api.views import (BrandCreateView, BrandDeleteView, BrandsListView,
                       BrandUpdateView, CustomerViewSet, OrderCreateView,
                       OrderDeleteView, OrdersListView, OrderUpdateView,
                       ProductCreateView, ProductDeleteView, ProductListView,
                       ProductOrderDetailView, ProductOrdersListView,
                       ProductUpdateView)

app_name = "api"
router = routers.DefaultRouter()
router.register("customers", CustomerViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="FusionStyle",
        default_version="v1",
        description="API for passing questions",
        term_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@admin.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", include(router.urls)),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="swagger_docs"),

    path("products/", ProductListView.as_view(), name="products_list"),
    path("product-create/", ProductCreateView.as_view(), name="product_create"),
    path("product-update/<int:pk>/", ProductUpdateView.as_view(), name="product_update"),
    path("product-delete/<int:pk>/", ProductDeleteView.as_view(), name="product_delete"),
    path("product-all-orders/<int:product_pk>/", ProductOrdersListView.as_view(), name="product_all_orders"),
    path(
        "product-detail-order/<int:product_pk>/order/<int:order_pk>/",
        ProductOrderDetailView.as_view(),
        name="product_detail_order",
    ),

    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("order-delete/<int:pk>/", OrderDeleteView.as_view(), name="order_delete"),
    path("order-update/<int:pk>/", OrderUpdateView.as_view(), name="order_update"),
    path("order-create/", OrderCreateView.as_view(), name="order_create"),

    path("brands/", BrandsListView.as_view(), name="brands_list"),
    path("brand-delete/<int:pk>/", BrandDeleteView.as_view(), name="brand_delete"),
    path("brand-update/<int:pk>/", BrandUpdateView.as_view(), name="brand_update"),
    path("brand-create/", BrandCreateView.as_view(), name="brand_create"),
]
