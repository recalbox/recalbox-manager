"""
Views for Bios views
"""
import os, re
from operator import itemgetter

from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from project.manager_frontend.forms.bios import BiosUploadForm

class BiosListView(FormView):
    template_name = "manager_frontend/bios_list.html"
    system_regex = re.compile(r"(-\s)(.*)(\s:)")
    md5hash_regex = re.compile(r"([a-fA-F\d]{32})")
    form_class = BiosUploadForm
            
    def get_bios_list(self):
        path = settings.RECALBOX_BIOS_PATH
        bios_dir_files = [item for item in os.listdir(path) if os.path.isfile(os.path.join(path, item)) and not item.startswith('.')]
        
        for item in self.bios_manifest:
            md5hash,filename,system,exist = item
            if filename in bios_dir_files:
                item[3] = True
        
        return bios_dir_files
    
    def get_bios_manifest(self):
        """
        Open the manifest to find knowed bios files
        """
        bios_list = []
        
        for system_key, system_datas in settings.RECALBOX_MANIFEST.items():
            system_name = system_datas.get('name', system_key)
            if len(system_datas.get('bios', []))>0:
                for md5hash,filename in system_datas['bios']:
                    bios_list.append([md5hash, filename, system_name, False])
                
        return sorted(bios_list, key=itemgetter(2, 1))
    
    def deprecated_get_bios_manifest(self):
        """
        Open the manifest file to find knowed bios files
        
        Parse the manifest using regex to find system and bios entries. This 
        assume the bios lines are correctly typed and ordered.
        
        DEPRECATED: this was the old dirty technic
        """
        bios_list = []
        
        current_system = 'Unknowed'
        
        with open(self.bios_manifest_file, 'rb') as file:
            for line in file:
                line = line.strip()
                system_match = self.system_regex.match(line)
                # Search for a system name
                if system_match is not None:
                    current_system = system_match.group(2)
                # Search for a bios file entry
                elif line:
                    m = self.md5hash_regex.match(line)
                    if m is not None:
                        md5hash,filename = line.split()
                        bios_list.append([md5hash,filename,current_system, False])
                
        return bios_list
    
    def get_context_data(self, **kwargs):
        context = super(BiosListView, self).get_context_data(**kwargs)
        context.update({
            'bios_path': settings.RECALBOX_BIOS_PATH,
            #'bios_manifest_file': self.bios_manifest_file,
            'bios_manifest': self.bios_manifest,
            'existing_bios_files': self.existing_bios_files,
            'existing_bios_length': len([True for item in self.bios_manifest if item[3]]),
        })
        return context
            
    def get_form_kwargs(self):
        context = super(BiosListView, self).get_form_kwargs()
        context.update({
            'bios_manifest': self.bios_manifest,
        })
        return context
        
    def init_manifest(self):
        self.bios_manifest = self.get_bios_manifest()
        self.existing_bios_files = self.get_bios_list()

    def form_valid(self, form):
        uploaded_file = form.save()
        
        # Throw a message to tell about upload success
        messages.success(self.request, _('File has been uploaded: {}').format(os.path.basename(uploaded_file)))
        
        return super(BiosListView, self).form_valid(form)

    def get_success_url(self):
        return reverse('manager:bios')
        
    def get(self, request, *args, **kwargs):
        self.init_manifest()
        return super(BiosListView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.init_manifest()
        return super(BiosListView, self).post(request, *args, **kwargs)
