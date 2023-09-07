from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from shop.models import Category, Product


class ProductListView(ListView):
    model = Product
    template_name = "products_list.html"
    context_object_name = "products"

    def get_queryset(self):
        product_category = self.kwargs.get("category")
        if product_category:
            category = get_object_or_404(Category, name=product_category)
            return Product.objects.filter(category=category)
        else:
            return Product.objects.all()


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"
