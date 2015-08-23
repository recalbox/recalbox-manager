# -*- coding: utf-8 -*-
"""
Thread forms
"""
import os, hashlib

from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import FileSystemStorage

from project.manager_frontend.forms import CrispyFormMixin
from project.utils.imports import safe_import_module

BIOS_FS_STORAGE = FileSystemStorage(location=settings.RECALBOX_BIOS_PATH, base_url=settings.MEDIA_URL)

def hashfile(afile, hasher, blocksize=65536):
    """
    Efficient way to generate checksum from a file, return hexdigest checksum
    
    Use it like this:
        
        import hashlib
        hashfile(open(BIOS_FS_STORAGE.path(YOUR_FILEPATH), 'rb'), hashlib.md5())
    
    Stealed from http://stackoverflow.com/a/3431835/4884485
    """
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()

class BiosUploadForm(CrispyFormMixin, forms.Form):
    """
    Bios upload form
    """
    #crispy_form_helper_path = 'project.manager_frontend.forms.crispies.bios_helper'
    #crispy_form_helper_kwargs = {}
    
    bios = forms.FileField(label=_('Bios file'), required=True)
    
    def __init__(self, *args, **kwargs):
        self.manifest = kwargs.pop('bios_manifest')
        
        super(BiosUploadForm, self).__init__(*args, **kwargs)
        super(forms.Form, self).__init__(*args, **kwargs)
        

    def clean_bios(self):
        """
        Validate bios file from Recalbox Manifest
        
        The bios file must have the right file name and the right md5 checksum
        """
        bios = self.cleaned_data['bios']
        if bios:
            simple_manifest = {filename: md5hash for (md5hash,filename,system_name,exists) in self.manifest}
            name = os.path.basename(bios.name)
            
            if name not in simple_manifest:
                raise forms.ValidationError(_("Your file does not seem to be a supported Bios"))
            else:
                bios_checksum = hashfile(bios, hashlib.md5())
                if bios_checksum != simple_manifest[name]:
                    raise forms.ValidationError(_("Your file does not have a correct MD5 checksum"))


        return bios
    
    def save(self):
        bios = self.cleaned_data["bios"]
        
        # Remove the previous file with identical name if any
        if BIOS_FS_STORAGE.exists(bios.name):
            BIOS_FS_STORAGE.delete(bios.name)
            
        # Save the new uploaded file
        BIOS_FS_STORAGE.save(bios.name, bios)
        
        return BIOS_FS_STORAGE.path(bios.name)
