"""
Views for configuration files
"""
from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.contrib import messages

from project.manager_frontend.forms.config import ConfigEditForm

class RecalboxConfigFormView(FormView):
    template_name = "manager_frontend/config_form.html"
    form_class = ConfigEditForm

    def dispatch(self, request, *args, **kwargs):
        self.config_filepath = settings.RECALBOX_CONF_PATH
        self.config_content = self.get_config_file()
        return super(RecalboxConfigFormView, self).dispatch(request, *args, **kwargs)
            
    def get_config_file(self):
        content = None
        
        with open(self.config_filepath, 'rb') as file:
            content = file.read()
            
        return content
    
    def get_context_data(self, **kwargs):
        context = super(RecalboxConfigFormView, self).get_context_data(**kwargs)
        context.update({
            'config_filepath': self.config_filepath,
            'config_content': self.config_content,
        })
        return context

    def get_success_url(self):
        return reverse('manager:config')
            
    def get_form_kwargs(self):
        context = super(RecalboxConfigFormView, self).get_form_kwargs()
        context.update({
            'config_filepath': self.config_filepath,
        })
        return context
    
    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        return {
            'content': self.config_content,
        }

    def form_valid(self, form):
        form.save()
        
        # Throw a message to tell about upload success
        messages.success(self.request, 'File has been edited')
        
        return super(RecalboxConfigFormView, self).form_valid(form)
