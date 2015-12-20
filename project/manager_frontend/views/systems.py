"""
Views for roms
"""
import os
from operator import itemgetter

from django.conf import settings
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _

from project.recalbox_manifest import manifest as RECALBOX_MANIFEST

from project.manager_frontend.forms.systems import SystemCreateForm

class SystemsListView(FormView):
    """
    List rom system folders
    """
    template_name = "manager_frontend/systems_list.html"
    form_class = SystemCreateForm
            
    def get_system_list(self):
        path = settings.RECALBOX_ROMS_PATH
        existing_sys = []
        available_sys = []
        
        # Get existing systems as directories
        for item in os.listdir(path):
            # Only display directories
            if os.path.isdir(os.path.join(path, item)) and not item.startswith('.'):
                # Try to find the dirname in the system manifest
                if item in RECALBOX_MANIFEST:
                    existing_sys.append( (item, RECALBOX_MANIFEST[item]['name']) )
                # Unknowed dirname
                else:
                    existing_sys.append( (item, item) )
        
        # Get system available: the ones that dont allready have a directory in systems dir
        for sys_key, sys_values in RECALBOX_MANIFEST.items():
            if sys_key not in [v[0] for v in existing_sys]:
                available_sys.append( (sys_key, sys_values['name']) )
        
        return (
            sorted(existing_sys, key=itemgetter(0)),
            sorted(available_sys, key=itemgetter(0)),
        )
            
    def get_context_data(self, **kwargs):
        context = super(SystemsListView, self).get_context_data(**kwargs)
        context.update({
            'systems_path': settings.RECALBOX_ROMS_PATH,
            'systems_list': self.existing_systems,
            'available_systems': self.available_systems,
        })
        return context
            
    def get_form_kwargs(self):
        context = super(SystemsListView, self).get_form_kwargs()
        context.update({
            'available_systems': self.available_systems,
        })
        return context
    
    def form_valid(self, form):
        new_system = form.save()
        
        # Throw a message to tell about upload success
        messages.success(self.request, _('System "{}" has been created').format(new_system['name']))
        
        return super(SystemsListView, self).form_valid(form)

    def get_success_url(self):
        return reverse('manager:roms-systems')
        
    def get(self, request, *args, **kwargs):
        self.existing_systems, self.available_systems = self.get_system_list()
        return super(SystemsListView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.existing_systems, self.available_systems = self.get_system_list()
        return super(SystemsListView, self).post(request, *args, **kwargs)
