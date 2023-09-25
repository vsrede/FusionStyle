import pprint

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DetailView, ListView,
                                  RedirectView, TemplateView)

from shop.forms import (OrderForm, ProductFilterForm,
                        ProductFilterWithCategoryForm)
from shop.models import Cart, CartItem, Category, Order, Product
from shop.tasks import generate_product_brand_category
from shop.utils.generate_unique_session_id import generate_unique_session_id
from shop.utils.sort_queryset_by_price import sort_queryset_by_price


class ProductListView(ListView):
    model = Product
    template_name = "products_list.html"
    context_object_name = "products"

    def get_queryset(self):
        product_category = self.kwargs.get("category")
        category = get_object_or_404(Category, name=product_category)
        queryset = Product.objects.filter(category=category)
        form = ProductFilterForm(self.request.GET)
        if form.is_valid():
            search = form.cleaned_data.get("search")
            brand = form.cleaned_data.get("brand")

            if search:
                queryset = queryset.filter(name__icontains=search)

            if brand:
                queryset = queryset.filter(brand=brand)
        sort_by = self.request.GET.get("sort_by")
        queryset = sort_queryset_by_price(queryset, sort_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProductFilterWithCategoryForm(self.request.GET)
        return context


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
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProductFilterWithCategoryForm(self.request.GET)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


class AddToCartView(View):
    def post(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        if request.user.is_authenticated:
            customer = request.user
            cart, created = Cart.objects.get_or_create(customer=customer)
        else:
            guest_session_id = request.session.get("guest_session_id")
            if not guest_session_id:
                guest_session_id = generate_unique_session_id()
                request.session["guest_session_id"] = guest_session_id
            customer = None

            cart, created = Cart.objects.get_or_create(guest_session_id=guest_session_id)

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
        cart_item = get_object_or_404(CartItem, product_id=product_id, cart__customer=self.request.user)

        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        return reverse("shop:cart")


class RemoveFromCartView(View):
    def post(self, request, product_id):
        cart_item = get_object_or_404(CartItem, product_id=product_id, cart__customer=request.user)
        cart_item.delete()
        return HttpResponseRedirect(reverse("shop:cart"))


class CreateOrderView(LoginRequiredMixin, CreateView):
    template_name = "create_order.html"
    form_class = OrderForm
    success_url = reverse_lazy("index")
    login_url = "index"

    def form_valid(self, form):
        current_user = self.request.user
        form.instance.customer = current_user

        # Сначала сохраните заказ в базе данных, чтобы получить значение "id"
        response = super().form_valid(form)

        # Затем получите продукты из корзины пользователя и добавьте их в заказ
        cart_items = current_user.cart.cart_items.all()
        self.object.products.set([item.product for item in cart_items])

        # Очистите корзину пользователя
        cart_items.delete()
        return response


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
    context_object_name = "products"
    login_url = "index"

    def get_queryset(self):
        order = get_object_or_404(Order, id=self.kwargs.get("order_id"))
        products = order.products.all()
        print(self.kwargs.get("order_id"))
        print(order.delivery_address)
        return products


def generate_instances_view(request):
    generate_product_brand_category.delay()
    return HttpResponse("Task generate instances is started")
