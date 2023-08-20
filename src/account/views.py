from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, RedirectView

from account.forms import UserRegistrationForm
from core.services.emails import send_registration_email
from core.utils.token_generator import TokenGenerator


class UserRegistrationView(CreateView):
    template_name = "create_account.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        send_registration_email(request=self.request, user_instance=user)
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
