# -*- coding: utf-8 -*-
"""
Thread forms
"""
import os

from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import FileSystemStorage

from project.manager_frontend.forms import CrispyFormMixin
from project.utils.imports import safe_import_module

ROMS_FS_STORAGE = FileSystemStorage(location=settings.RECALBOX_ROMS_PATH, base_url=settings.MEDIA_URL)

class RomDeleteForm(CrispyFormMixin, forms.Form):
    """
    Form to delete many roms
    """
    form_key = 'delete'
    form_fieldname_trigger = 'delete_submit'
    
    #crispy_form_helper_path = 'project.manager_frontend.forms.crispies.rom_delete_helper'
    #crispy_form_helper_kwargs = {}
    
    def __init__(self, *args, **kwargs):
        self.system = kwargs.pop('system')
        self.romchoices = kwargs.pop('romchoices')
        
        super(RomDeleteForm, self).__init__(*args, **kwargs)
        super(forms.Form, self).__init__(*args, **kwargs)
        
        self.fields['roms'] = forms.MultipleChoiceField(choices=self.romchoices, widget=forms.CheckboxSelectMultiple, required=False)
    
    def save(self):
        roms = self.cleaned_data["roms"]
        delete_roms = []
        
        # Delete all selected rom files
        for filename in roms:
            system_relative_path = os.path.join(self.system, filename)
            
            if ROMS_FS_STORAGE.exists(system_relative_path):
                ROMS_FS_STORAGE.delete(system_relative_path)
                delete_roms.append(system_relative_path)
        
        return delete_roms


class RomUploadForm(CrispyFormMixin, forms.Form):
    """
    Rom upload form
    """
    #crispy_form_helper_path = 'project.manager_frontend.forms.crispies.rom_upload_helper'
    #crispy_form_helper_kwargs = {}
    form_key = 'upload'
    form_fieldname_trigger = 'upload_submit'
    
    rom = forms.FileField(label=_('Rom file'), required=True)
    
    def __init__(self, *args, **kwargs):
        self.system = kwargs.pop('system')
        self.system_manifest = kwargs.pop('system_manifest')
        
        super(RomUploadForm, self).__init__(*args, **kwargs)
        super(forms.Form, self).__init__(*args, **kwargs)
        

    def clean_rom(self):
        """
        Validate rom file
        """
        rom = self.cleaned_data['rom']
        if rom:
            root, ext = os.path.splitext(rom.name)
            if ext.startswith('.'):
                ext = ext[1:]
            if self.system_manifest['extensions'] and len(self.system_manifest['extensions'])>0 and ext not in self.system_manifest['extensions']:
                raise forms.ValidationError(_("Your file does not seem to be a valid Rom for this system"))

        return rom
    
    def save(self):
        rom = self.cleaned_data["rom"]
        system_relative_path = os.path.join(self.system, rom.name)
        
        # Remove the previous file with identical name if any
        if ROMS_FS_STORAGE.exists(system_relative_path):
            ROMS_FS_STORAGE.delete(system_relative_path)
            
        # Save the new uploaded file
        ROMS_FS_STORAGE.save(system_relative_path, rom)
        
        return ROMS_FS_STORAGE.path(system_relative_path)
