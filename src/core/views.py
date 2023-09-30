from django.conf import settings
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["google_maps_api_key"] = settings.GOOGLE_MAPS_API_KEY
        return context


class PageNotFondView(TemplateView):
    template_name = "404.html"
    http_method_names = ["get"]
