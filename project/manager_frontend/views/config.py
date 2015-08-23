"""
Views for configuration files
"""
from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView

class RecalboxConfigFormView(TemplateView):
    template_name = "manager_frontend/config_form.html"
            
    def get_config_file(self):
        content = None
        
        with open(settings.RECALBOX_CONF_PATH, 'rb') as file:
            content = file.read()
            
        return content
    
    def get_context_data(self, **kwargs):
        context = super(RecalboxConfigFormView, self).get_context_data(**kwargs)
        context.update({
            'config_filepath': settings.RECALBOX_CONF_PATH,
            'config_content': self.get_config_file(),
        })
        return context
