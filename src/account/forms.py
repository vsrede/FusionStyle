from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from account.models import Customer


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ["email", "password1", "password2", "first_name", "last_name"]


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = Customer
        fields = [
            "email",
            "first_name",
            "last_name",
            "avatar",
            "phone_number",
            "address",
            "city",
            "zipcode",
            "country",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("password")
