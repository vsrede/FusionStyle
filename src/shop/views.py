import json
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Model
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DetailView, ListView,
                                  RedirectView, TemplateView)

from shop.forms import OrderForm, ProductFilterWithCategoryForm
from shop.models import (Cart, CartItem, Favorite, GuestCart, Order, OrderItem,
                         Product)
from shop.tasks import generate_product_brand_category
from shop.utils.decimal import DecimalEncoder
from shop.utils.generate_unique_session_id import generate_unique_session_id
from shop.utils.sort_queryset_by_price import sort_queryset_by_price


class ProductAllListView(ListView):
    model = Product
    template_name = "products_all_list.html"
    context_object_name = "products"
    queryset = Product.objects.all()
    ordering = "-price"

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ProductFilterWithCategoryForm(self.request.GET)

        if form.is_valid():
            search = form.cleaned_data.get("search")
            category = form.cleaned_data.get("category")
            brand = form.cleaned_data.get("brand")

            if search:
                queryset = queryset.filter(name__icontains=search)

            if category:
                queryset = queryset.filter(category=category)

            if brand:
                queryset = queryset.filter(brand=brand)

        sort_by = self.request.GET.get("sort_by")
        queryset = sort_queryset_by_price(queryset, sort_by)

        queryset_values = list(queryset.values())
        queryset_values_serializable = []
        for item in queryset_values:
            serialized_item = {}
            for key, value in item.items():
                if isinstance(value, Model):
                    serialized_item[key] = model_to_dict(
                        value, fields=["id", "name"]
                    )
                elif isinstance(value, datetime):
                    serialized_item[key] = value.strftime("%Y-%m-%dT%H:%M:%SZ")
                else:
                    serialized_item[key] = value

            queryset_values_serializable.append(serialized_item)

        serialized_data = json.dumps(queryset_values_serializable, cls=DecimalEncoder)

        self.request.session["queryset_values"] = serialized_data

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProductFilterWithCategoryForm(self.request.GET)
        context["product_category"] = self.kwargs.get("category")
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


class AddToCartView(View):
    def post(self, request, product_id):
        product = Product.objects.get(pk=product_id)

        cart = None

        if request.user.is_authenticated:
            customer = request.user
            cart, created = Cart.objects.get_or_create(customer=customer)

            guest_session_id = request.session.get("guest_session_id")
            if guest_session_id:
                guest_cart = GuestCart.objects.filter(session_key=guest_session_id).first()
                if guest_cart:
                    for guest_cart_item in guest_cart.guestcartitem_set.all():
                        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=guest_cart_item.product)
                        if not created:
                            cart_item.quantity += guest_cart_item.quantity
                            cart_item.save()
                    guest_cart.delete()
                    del request.session["guest_session_id"]
        else:
            guest_session_id = request.session.get("guest_session_id")
            if not guest_session_id:
                guest_session_id = generate_unique_session_id()
                request.session["guest_session_id"] = guest_session_id
            customer = None

            request.session["cart_details"] = {
                "guest_session_id": guest_session_id,
                "cart_items": [
                    {"product_id": item.product.id, "quantity": item.quantity}
                    for item in CartItem.objects.filter(cart__guest_session_id=guest_session_id)
                ],
            }

            cart, created = Cart.objects.get_or_create(customer=None, guest_session_id=guest_session_id)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect("shop:cart")


class CartView(TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            customer = self.request.user
            cart, created = Cart.objects.get_or_create(customer=customer)
        else:
            guest_session_id = self.request.session.get("guest_session_id")
            if not guest_session_id:
                guest_session_id = generate_unique_session_id()
                self.request.session["guest_session_id"] = guest_session_id
            customer = None
            cart, created = Cart.objects.get_or_create(guest_session_id=guest_session_id)

        cart_items = cart.cart_items.all()
        context["cart"] = cart
        context["cart_items"] = cart_items

        total_items = cart.total_items()
        context["total_items"] = total_items

        total_price = cart.total_price()
        context["total_price"] = total_price

        return context


class UpdateCartView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        product_id = kwargs["product_id"]
        quantity = int(self.request.POST.get("quantity"))

        if self.request.user.is_authenticated:
            cart_item = get_object_or_404(CartItem, product_id=product_id, cart__customer=self.request.user)

            if quantity <= 0:
                cart_item.delete()
            else:
                cart_item.quantity = quantity
                cart_item.save()

        else:
            guest_session_id = self.request.session.get("guest_session_id")
            if guest_session_id:
                cart_item = get_object_or_404(CartItem, product_id=product_id, cart__guest_session_id=guest_session_id)

                if quantity <= 0:
                    cart_item.delete()
                else:
                    cart_item.quantity = quantity
                    cart_item.save()

        return self.request.META.get("HTTP_REFERER", reverse("shop:cart"))


class RemoveFromCartView(View):
    def post(self, request, product_id):
        if request.user.is_authenticated:
            cart_item = get_object_or_404(CartItem, product_id=product_id, cart__customer=request.user)
            cart_item.delete()
        else:
            guest_session_id = request.session.get("guest_session_id")
            if guest_session_id:
                cart_item = get_object_or_404(CartItem, product_id=product_id, cart__guest_session_id=guest_session_id)
                cart_item.delete()

        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


class CreateOrderView(LoginRequiredMixin, CreateView):
    template_name = "create_order.html"
    form_class = OrderForm
    success_url = reverse_lazy("index")
    login_url = "index"

    def form_valid(self, form):
        current_user = self.request.user
        form.instance.customer = current_user

        if current_user.is_authenticated:
            cart, created = Cart.objects.get_or_create(customer=current_user)
        else:
            guest_session_id = self.request.session.get("guest_session_id")
            cart, created = Cart.objects.get_or_create(guest_session_id=guest_session_id)

        cart_items = cart.cart_items.all()
        form.instance.cart = cart
        form.save()

        if cart_items.exists():
            for cart_item in cart_items:
                OrderItem.objects.create(order=form.instance, product=cart_item.product, quantity=cart_item.quantity)

            cart_items.delete()
        return super().form_valid(form)


class OrdersListView(LoginRequiredMixin, ListView):
    template_name = "orders_list.html"
    context_object_name = "orders"
    login_url = "index"

    def get_queryset(self):
        user = get_object_or_404(get_user_model(), pk=self.kwargs.get("pk"))
        queryset = user.order_set.all()
        return queryset


class OrderDetailListView(LoginRequiredMixin, ListView):
    template_name = "order_detail_list.html"
    context_object_name = "order_items"
    login_url = "index"

    def get_queryset(self):
        order = get_object_or_404(Order, id=self.kwargs.get("order_id"))
        return order.orderitem_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_object_or_404(Order, id=self.kwargs.get("order_id"))
        context["order_items"] = order.orderitem_set.all()
        return context


class AddFavoriteView(LoginRequiredMixin, CreateView):
    model = Favorite
    fields = []

    def form_valid(self, form):
        product = get_object_or_404(Product, id=self.kwargs["product_id"])
        form.instance.user = self.request.user
        form.instance.product = product
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("shop:product_detail", args=[self.kwargs["product_id"]])


class FavoriteListView(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = "favorites.html"
    context_object_name = "favorites"
    paginate_by = 10

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).order_by()


def remove_favorite(request, product_id):
    if request.method == "POST":
        favorites = Favorite.objects.filter(user=request.user, product_id=product_id)

        if favorites.exists():
            favorite_to_remove = favorites.first()
            favorite_to_remove.delete()
            return redirect("shop:favorite_list")
        else:
            return HttpResponse("Favorite not found", status=404)
    else:
        return HttpResponse("Method not allowed", status=405)


def generate_instances_view(request):
    generate_product_brand_category.delay()
    return HttpResponse("Task generate instances is started")
