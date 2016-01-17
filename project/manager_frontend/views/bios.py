"""
Views for Bios views
"""
import os
from operator import itemgetter

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import Http404, HttpResponseBadRequest
from django.utils.translation import ugettext as _

from project.utils.views import JsonMixin

from project.recalbox_manifest import manifest as RECALBOX_MANIFEST

from project.manager_frontend.forms.bios import BiosDeleteForm, BiosUploadForm
from project.manager_frontend.utils.views import MultiFormView

class BiosListView(MultiFormView):
    """
    List supported Bios from Recalbox manifest
    
    Include an upload form to add valid bios file and a delete form to remove 
    some existing bios.
    """
    template_name = "manager_frontend/bios_list.html"
    enabled_forms = (BiosUploadForm, BiosDeleteForm)
            
    def init_manifest(self):
        self.bios_manifest = self.get_bios_manifest()
        self.existing_bios_files = self.get_existing_bios_list()

    def get_existing_bios_list(self):
        """
        Walk into Bios directory to find existing files for knowed bios (from manifest)
        """
        path = settings.RECALBOX_BIOS_PATH
        bios_dir_files = [item for item in os.listdir(path) if os.path.isfile(os.path.join(path, item)) and not item.startswith('.')]
        
        for md5hash,values in self.bios_manifest.items():
            filename,system,exist = values
            if filename in bios_dir_files:
                values[2] = True
        
        return bios_dir_files
    
    def get_bios_manifest(self):
        """
        Open the manifest to find knowed bios files
        """
        bios_dict = {}
        
        for system_key, system_datas in RECALBOX_MANIFEST.items():
            system_name = system_datas.get('name', system_key)
            if len(system_datas.get('bios', []))>0:
                for md5hash,filename in system_datas['bios']:
                    bios_dict[md5hash] = [filename, system_name, False]
                
        return bios_dict
            
    def get_bios_choices(self):
        rom_list = []
        
        for md5hash,values in self.bios_manifest.items():
            rom_list.append( (md5hash, values[0]) )
        
        return tuple( sorted(rom_list, key=itemgetter(1)) )
    
    def get_context_data(self, **kwargs):
        context = super(BiosListView, self).get_context_data(**kwargs)
        context.update({
            'bios_path': settings.RECALBOX_BIOS_PATH,
            'bios_manifest': self.bios_manifest,
            'existing_bios_files': self.existing_bios_files,
            'existing_bios_length': len([True for md5hash,values in self.bios_manifest.items() if values[2]]),
        })
        return context
            
    def get_upload_form_kwargs(self, kwargs):
        kwargs.update({'bios_manifest': self.bios_manifest})
        return kwargs
    
    def get_delete_form_kwargs(self, kwargs):
        kwargs.update({'bios_choices': self.get_bios_choices()})
        return kwargs
        
    def upload_form_valid(self, form):
        uploaded_file = form.save()
        
        # Throw a message to tell about upload success
        messages.success(self.request, _('File has been uploaded: {}').format(os.path.basename(uploaded_file)))
            
    def delete_form_valid(self, form):
        deleted_files = form.save()
        if deleted_files and len(deleted_files)>0:
            deleted_files = ", ".join([os.path.basename(item) for item in deleted_files])
            # Throw a message to tell about deleted files
            messages.success(self.request, _('Deleted file(s): {}').format( deleted_files ))

    def get_success_url(self):
        return reverse('manager:bios')
        
    def get(self, request, *args, **kwargs):
        self.init_manifest()
        return super(BiosListView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.init_manifest()
        return super(BiosListView, self).post(request, *args, **kwargs)


class BiosUploadJsonView(JsonMixin, BiosListView):
    """
    Inherit from BiosListView to be similary but gives only response in JSON
    
    Also the delete form should not really be used here
    """
    def upload_form_valid(self, form):
        """
        Return a dummy success response suitable to Dropzone plugin
        """
        uploaded_file = form.save()
        
        return self.json_response({'status': 'success'})

    def form_invalid(self, *args):
        """
        Tricky error JSON response for upload
        
        This is a naive implementation than assume this is only about bios upload 
        form errors.
        """
        forms_errors = {'error': 'Unknow error occured'}
        error_msg = ''
        
        for form in args:
            # Bother only about upload form
            if form.form_key == 'upload':
                errs = form.errors.as_data()
                # Get error(s), potentially compact them if more than one message
                if 'bios' in errs:
                    error_context = [str(item.message) for item in errs['bios']]
                    if len(error_context) > 1:
                        error_msg = "\n".join(error_context)
                    elif len(error_context) == 1:
                        error_msg = "".join(error_context)
            else:
                continue
        
        if error_msg:
            forms_errors['error'] = error_msg
        
        return self.json_response(forms_errors, response_klass=HttpResponseBadRequest)
