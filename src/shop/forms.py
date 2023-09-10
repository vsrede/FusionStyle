from django.forms import ModelForm

from shop.models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["customer", "status", "products"]
