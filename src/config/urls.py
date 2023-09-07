from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from core.views import IndexView, PageNotFondView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path("account/", include("account.urls")),
    path("oauth/", include("social_django.urls", namespace="social")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("api.urls")),
    path("shop/", include("shop.urls")),
]
handler404 = PageNotFondView.as_view()


# delete ->
# put -> для зміни, але відправити треба весь набір даних
# patch -> для зміни одного рядка записів
# post -> створення
# get -> витягування
# options ->
