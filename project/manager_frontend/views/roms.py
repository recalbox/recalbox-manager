"""
Views for roms
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

from project.manager_frontend.forms.roms import RomUploadForm, RomDeleteForm
from project.manager_frontend.utils.views import MultiFormView


class RomListView(MultiFormView):
    """
    List rom from a system folder with an upload form and delete form
    
    This is a huge rewrite and mixing of some CBV views and mixins to be able 
    to distinctly manage the two forms
    
    Upload form part is only used with browser that dont accept Javascript, others 
    use the Dropzone plugin and so are routed to 'RomUploadJsonView'.
    """
    template_name = "manager_frontend/rom_list.html"
    enabled_forms = (RomUploadForm, RomDeleteForm)
            
    def init_system(self):
        self.system_key = self.kwargs.get('system')
        self.system_path = os.path.join(settings.RECALBOX_ROMS_PATH, self.system_key)
        
        # Only display existing and not hidded directories
        if not os.path.exists(self.system_path) or not os.path.isdir(self.system_path) or self.system_key.startswith('.'):
            raise Http404
        
        default_manifest = settings.RECALBOX_SYSTEM_DEFAULT
        default_manifest.update({
            'key': self.system_key,
            'name': self.system_key
        })
        # Get the system manifest part if any, else a default dict
        self.system_manifest = RECALBOX_MANIFEST.get(self.system_key, default_manifest)
            
    def get_rom_choices(self, force=False):
        """
        Return rom files as a choice list for form
        
        Don't list hided files and directories.
        
        If system is a supported system in manifest, filter files so only 
        supported rom type is listed, else dont filter on file extension.
        
        Use some internal memory cache to not digg the dir each time, use 
        force=True to bypass the cache
        """
        cache_key = '_get_rom_choices_cache'
        if force or not hasattr(self, cache_key):
            rom_list = []
            system_extensions = ['.{}'.format(k) for k in self.system_manifest.get('extensions', [])]
            
            for item in os.listdir(self.system_path):
                try:
                    if os.path.isfile(os.path.join(self.system_path, item)) and not item.startswith('.'):
                        if system_extensions and os.path.splitext(item)[-1]  not in system_extensions:
                            continue
                        rom_list.append( (item, os.path.getsize(os.path.join(self.system_path, item))) )
                # Issue #39: Naive fix to avoid throwing exception on bad encoded 
                #            filename, just ignore it and continue.
                except UnicodeDecodeError:
                    continue
            
            setattr(self, cache_key, tuple( sorted(rom_list, key=itemgetter(0)) ))
        
        return getattr(self, cache_key)
            
    def get_context_data(self, **kwargs):
        context = super(RomListView, self).get_context_data(**kwargs)
        context.update({
            'system': self.system_key,
            'system_path': self.system_path,
            'system_name': self.system_manifest['name'],
            'system_manifest': self.system_manifest,
            'total_roms': len(self.get_rom_choices()),
        })
        return context

    def check_system_bios(self):
        """
        Use manifest for bios systems and check if they exists on FS
        
        Return a list of bios filenames that are missing if any
        """
        if self.system_manifest.get('bios', False):
            missing = []
            bios_filenames = [v for k,v in self.system_manifest['bios']]
            for item in bios_filenames:
                if not os.path.exists(os.path.join(settings.RECALBOX_BIOS_PATH, item)):
                    missing.append(item)
            return missing
            
        return None

    def get_success_url(self):
        return reverse('manager:roms-list', args=[self.kwargs.get('system')])
    
    def get_upload_form_kwargs(self, kwargs):
        kwargs.update({
            'system_manifest': self.system_manifest,
            'system': self.system_key,
        })
        return kwargs
    
    def get_delete_form_kwargs(self, kwargs):
        kwargs.update({
            'romchoices': self.get_rom_choices(),
            'system': self.system_key,
        })
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
        
    def get(self, request, *args, **kwargs):
        self.init_system()
        return super(RomListView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.init_system()
        return super(RomListView, self).post(request, *args, **kwargs)



class RomUploadJsonView(JsonMixin, RomListView):
    """
    Inherit from RomListView to be similary but only response in JSON
    
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
        
        This is a naive implementation than assume this is only about rom upload 
        form errors.
        """
        forms_errors = {'error': 'Unknow error occured'}
        error_msg = ''
        
        for form in args:
            # Bother only about upload form
            if form.form_key == 'upload':
                errs = form.errors.as_data()
                # Get error(s), potentially compact them if more than one message
                if 'rom' in errs:
                    error_context = [str(item.message) for item in errs['rom']]
                    if len(error_context) > 1:
                        error_msg = "\n".join(error_context)
                    elif len(error_context) == 1:
                        error_msg = "".join(error_context)
            else:
                continue
        
        if error_msg:
            forms_errors['error'] = error_msg
        
        return self.json_response(forms_errors, response_klass=HttpResponseBadRequest)
