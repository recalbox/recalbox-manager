"""
Views for roms
"""
import os
from operator import itemgetter

from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from project.manager_frontend.forms.roms import RomUploadForm

class SystemsListView(TemplateView):
    """
    List rom system folders
    """
    template_name = "manager_frontend/systems_list.html"
            
    def get_system_list(self):
        path = settings.RECALBOX_ROMS_PATH
        system_dirs = []
        for item in os.listdir(path):
            # Only display directories
            if os.path.isdir(os.path.join(path, item)) and not item.startswith('.'):
                # Try to find the dirname in the system manifest
                if item in settings.RECALBOX_MANIFEST:
                    system_dirs.append( (item, settings.RECALBOX_MANIFEST[item]['name']) )
                # Unknowed dirname
                else:
                    system_dirs.append( (item, item) )
        
        return sorted(system_dirs, key=itemgetter(0))
            
    def get_context_data(self, **kwargs):
        context = super(SystemsListView, self).get_context_data(**kwargs)
        context.update({
            'systems_path': settings.RECALBOX_ROMS_PATH,
            'systems_list': self.get_system_list(),
        })
        return context

class RomListView(FormView):
    """
    List rom from a system folder
    """
    template_name = "manager_frontend/rom_list.html"
    form_class = RomUploadForm
            
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
        self.system_manifest = settings.RECALBOX_MANIFEST.get(self.system_key, default_manifest)
            
    def get_rom_list(self):
        rom_list = [(item, os.path.getsize(os.path.join(self.system_path, item))) for item in os.listdir(self.system_path) 
                    if os.path.isfile(os.path.join(self.system_path, item)) and not item.startswith('.')]
        
        return sorted(rom_list, key=itemgetter(0))
            
    def get_context_data(self, **kwargs):
        context = super(RomListView, self).get_context_data(**kwargs)
        context.update({
            'system': self.system_key,
            'system_path': self.system_path,
            'system_name': self.system_manifest['name'],
            'system_manifest': self.system_manifest,
            'rom_list': self.get_rom_list(),
        })
        return context
            
    def get_form_kwargs(self):
        context = super(RomListView, self).get_form_kwargs()
        context.update({
            'system': self.system_key,
            'system_manifest': self.system_manifest,
        })
        return context
        
    def get(self, request, *args, **kwargs):
        self.init_system()
        return super(RomListView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.init_system()
        return super(RomListView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        uploaded_file = form.save()
        
        # Throw a message to tell about upload success
        messages.success(self.request, _('File has been uploaded: {}').format(os.path.basename(uploaded_file)))
        
        return super(RomListView, self).form_valid(form)

    def get_success_url(self):
        return reverse('manager:roms-list', args=[self.kwargs.get('system')])
