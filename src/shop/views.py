from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DetailView, ListView,
                                  RedirectView, TemplateView)

from shop.forms import OrderForm
from shop.models import Cart, CartItem, Category, Order, Product


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


class AddToCartView(LoginRequiredMixin, View):
    login_url = "index"

    def post(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        customer = request.user
        cart, created = Cart.objects.get_or_create(customer=customer)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect("shop:cart")


class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart.html"
    login_url = "index"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user
        cart, created = Cart.objects.get_or_create(customer=customer)
        cart_items = cart.cart_items.all()
        context["cart"] = cart
        context["cart_items"] = cart_items

        total_items = cart.total_items()
        context["total_items"] = total_items

        total_price = cart.total_price()
        context["total_price"] = total_price

        return context


class UpdateCartView(LoginRequiredMixin, RedirectView):
    permanent = False
    login_url = "index"

    def get_redirect_url(self, *args, **kwargs):
        product_id = kwargs["product_id"]
        quantity = int(self.request.POST.get("quantity"))
        cart_item = get_object_or_404(CartItem, product_id=product_id, cart__customer=self.request.user)

        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        return reverse("shop:cart")


class RemoveFromCartView(LoginRequiredMixin, View):
    login_url = "index"

    def post(self, request, product_id):
        cart_item = get_object_or_404(CartItem, product_id=product_id, cart__customer=request.user)
        cart_item.delete()
        return HttpResponseRedirect(reverse("shop:cart"))


class CreateOrderView(LoginRequiredMixin, CreateView):
    ...
