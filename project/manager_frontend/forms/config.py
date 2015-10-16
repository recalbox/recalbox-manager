# -*- coding: utf-8 -*-
"""
Recalbox Configuration forms
"""
import os

from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import FileSystemStorage

from project.manager_frontend.forms import CrispyFormMixin
from project.utils.imports import safe_import_module

class ConfigEditForm(CrispyFormMixin, forms.Form):
    """
    Configuration Edit form
    """
    #crispy_form_helper_path = 'project.manager_frontend.forms.crispies.config_helper'
    #crispy_form_helper_kwargs = {}
    
    content = forms.CharField(label=_('Content'), widget=forms.Textarea(attrs={'rows': 50}), required=True)
    backup = forms.BooleanField(label=_('Backup previous version before saving'), required=False)
    
    def __init__(self, *args, **kwargs):
        self.config_filepath = kwargs.pop('config_filepath')
        self.backup_filepath = kwargs.pop('backup_filepath')
        
        super(ConfigEditForm, self).__init__(*args, **kwargs)
        super(forms.Form, self).__init__(*args, **kwargs)
    
    def save(self):
        content = self.cleaned_data["content"]
        backup = self.cleaned_data["backup"]
        
        # Optionnal backup
        if backup:
            # Remove the previous backup file if any
            if os.path.exists(self.backup_filepath):
                os.remove(self.backup_filepath)
            # Then backup from the current one
            os.rename(self.config_filepath, self.backup_filepath)
        
        # Write the new configuration file
        with open(self.config_filepath, 'wb') as file:
            file.write(content.replace('\r\n', '\n').encode('UTF-8'))
       
        return content, backup
