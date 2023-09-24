from django import forms

from shop.models import Brand, Category, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["delivery_address", "delivery_first_name", "delivery_last_name"]


class ProductFilterForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter model name"}),
    )
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        required=False,
        empty_label="Select brand",
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class ProductFilterWithCategoryForm(ProductFilterForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Select category",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
