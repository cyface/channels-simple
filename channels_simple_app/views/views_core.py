"""Django Views"""
from django.views.generic import TemplateView


class HomePage(TemplateView):
    """Display Home Page"""
    template_name = 'home.html'
