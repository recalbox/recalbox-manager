"""
Views for configuration files
"""
import os

from django.conf import settings
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _

from project.manager_frontend.forms.config import ConfigEditForm

class RecalboxConfigFormView(FormView):
    """
    Display a form to edit the Recalbox config file
    """
    template_name = "manager_frontend/config_form.html"
    form_class = ConfigEditForm

    def dispatch(self, request, *args, **kwargs):
        self.config_filepath = settings.RECALBOX_CONF_PATH
        self.config_content = self.get_config_file(self.config_filepath)
        
        self.backup_filepath = settings.RECALBOX_CONF_BACKUP_PATH
        self.backup_content = None
        if os.path.exists(self.backup_filepath):
            self.backup_content = self.get_config_file(self.backup_filepath)
        
        return super(RecalboxConfigFormView, self).dispatch(request, *args, **kwargs)
            
    def get_config_file(self, filepath):
        content = None
            
        if filepath:
            with open(filepath, 'rb') as file:
                content = file.read()
        
        return content
    
    def get_context_data(self, **kwargs):
        context = super(RecalboxConfigFormView, self).get_context_data(**kwargs)
        context.update({
            'config_filepath': self.config_filepath,
            'config_content': self.config_content,
            'backup_filepath': self.backup_filepath,
            'backup_content': self.backup_content,
        })
        return context

    def get_success_url(self):
        return reverse('manager:config')
            
    def get_form_kwargs(self):
        context = super(RecalboxConfigFormView, self).get_form_kwargs()
        context.update({
            'config_filepath': self.config_filepath,
            'backup_filepath': self.backup_filepath,
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
        new_content, is_backuped = form.save()
        
        # Throw a message to tell about upload success
        if is_backuped:
            messages.success(self.request, _('File has been backuped then edited'))
        else:
            messages.success(self.request, _('File has been edited'))
        
        return super(RecalboxConfigFormView, self).form_valid(form)
