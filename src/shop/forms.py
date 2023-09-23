from django import forms

from shop.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["delivery_address", "delivery_first_name", "delivery_last_name"]
