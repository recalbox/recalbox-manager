# -*- coding: utf-8 -*-
"""
Recalbox Configuration forms
"""
import os

from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import FileSystemStorage

from project.recalbox_manifest import manifest as RECALBOX_MANIFEST

from project.manager_frontend.forms import CrispyFormMixin

from project.utils.imports import safe_import_module

#class SystemCreateForm(CrispyFormMixin, forms.Form):
class SystemCreateForm(forms.Form):
    """
    Create a new system directory
    """
    #crispy_form_helper_path = 'project.manager_frontend.forms.crispies.system_helper'
    #crispy_form_helper_kwargs = {}
    
    def __init__(self, *args, **kwargs):
        self.available_systems = kwargs.pop('available_systems')
        
        super(SystemCreateForm, self).__init__(*args, **kwargs)
        #super(forms.Form, self).__init__(*args, **kwargs)
        
        self.fields['name'] = forms.ChoiceField(label=_('Add a new system'), choices=self.available_systems, required=True)
    
    def save(self):
        name = self.cleaned_data["name"]
        
        os.mkdir(os.path.join(settings.RECALBOX_ROMS_PATH, name), 0755)
        
        return RECALBOX_MANIFEST[name]
