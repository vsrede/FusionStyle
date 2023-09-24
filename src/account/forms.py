from django.contrib.auth.forms import UserCreationForm

from account.models import Customer


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ["email", "password1", "password2", "first_name", "last_name"]
