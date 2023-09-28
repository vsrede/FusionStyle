from django.urls import path

from account.views import (AccountActivateView, AccountLoginView,
                           AccountLogoutView, ProfileView, UpdateUserView,
                           UserRegistrationView)

app_name = "account"

urlpatterns = [
    path("create/", UserRegistrationView.as_view(), name="create_account"),
    path("activate_account/<str:uuid64>/<str:token>/", AccountActivateView.as_view(), name="activate_account"),
    path("logout/", AccountLogoutView.as_view(), name="logout"),
    path("login/", AccountLoginView.as_view(), name="login"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path("update_user/<int:pk>/", UpdateUserView.as_view(), name="update_user"),
]
