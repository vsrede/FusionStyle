from django.urls import reverse_lazy
from django.views.generic import CreateView

from account.forms import UserRegistrationForm
from core.services.emails import send_registration_email


class UserRegistrationView(CreateView):
    template_name = "user_create.html"
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
