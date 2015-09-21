from django.views.generic import TemplateView

class HomeView(TemplateView):
    """
    Homepage view is actually only a "direct render to template"
    """
    template_name = "manager_frontend/home.html"
 