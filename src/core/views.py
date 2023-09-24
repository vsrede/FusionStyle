from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"
    http_method_names = ["get"]


class PageNotFondView(TemplateView):
    template_name = "404.html"
    http_method_names = ["get"]
