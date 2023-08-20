from django.urls import path

from account.views import UserRegistrationView, AccountActivateView, AccountLogoutView, AccountLoginView

app_name = "account"

urlpatterns = [
    path("create/", UserRegistrationView.as_view(), name="create_account"),
    path("activate_account/<str:uuid64>/<str:token>/", AccountActivateView.as_view(), name="activate_account"),
    path("logout/", AccountLogoutView.as_view(), name="logout"),
    path("login/", AccountLoginView.as_view(), name="login"),
]
