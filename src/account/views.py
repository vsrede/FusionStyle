from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import (CreateView, DetailView, RedirectView,
                                  UpdateView)

from account.forms import UserRegistrationForm, UserUpdateForm
from account.models import Customer
from account.utils.merge_guest_cart_with_user_cart import \
    merge_guest_cart_with_user_cart
from core.services.emails import send_registration_email
from core.utils.token_generator import TokenGenerator
from shop.models import Cart, CartItem


class UserRegistrationView(CreateView):
    template_name = "create_account.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        send_registration_email(request=self.request, user_instance=user)
        merge_guest_cart_with_user_cart(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AccountActivateView(RedirectView):
    url = reverse_lazy("index")
    template_name = "emails/wrong_data.html"

    def get(self, request, uuid64, token, *args, **kwargs):
        try:
            pk = force_str(urlsafe_base64_decode(uuid64))
            current_user = get_user_model().objects.get(pk=pk)
        except (get_user_model().DoesNotExist, TypeError, ValueError):
            return render(request, self.template_name)

        if current_user and TokenGenerator().check_token(current_user, token):
            current_user.is_active = True
            current_user.save()
            login(request, current_user, backend="django.contrib.auth.backends.ModelBackend")

            return super().get(request, *args, **kwargs)
        return render(request, self.template_name)


class AccountLogoutView(LogoutView):
    ...


class AccountLoginView(LoginView):
    template_name = "login.html"

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.user.is_authenticated:
            guest_session_id = self.request.session.get("guest_session_id")
            if guest_session_id:
                guest_cart = Cart.objects.filter(guest_session_id=guest_session_id).first()
                if guest_cart:
                    user_cart, created = Cart.objects.get_or_create(customer=self.request.user)
                    cart_items = guest_cart.cart_items.all()  # NOQA
                    for guest_cart_item in guest_cart.cart_items.all():
                        cart_item, created = CartItem.objects.get_or_create(
                            cart=user_cart, product=guest_cart_item.product
                        )
                        if not created:
                            cart_item.quantity += guest_cart_item.quantity
                            cart_item.save()
                    guest_cart.delete()
                    del self.request.session["guest_session_id"]

        return response


class ProfileView(DetailView):
    model = Customer
    template_name = "profile.html"
    context_object_name = "user_info"
    queryset = Customer.objects.all()


class UpdateUserView(LoginRequiredMixin, UpdateView):
    model = Customer
    template_name = "user_update.html"
    login_url = "index"
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse_lazy("account:profile", kwargs={"pk": self.object.pk})
