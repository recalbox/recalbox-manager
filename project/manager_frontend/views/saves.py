"""
Views for rom saves
"""
import json

import os, glob
from operator import itemgetter
from collections import OrderedDict, defaultdict

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import Http404, HttpResponseBadRequest
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from project.utils import keynat
from project.utils.views import JsonMixin

from project.recalbox_manifest import manifest as RECALBOX_MANIFEST

from project.manager_frontend.forms.roms import RomUploadForm, RomDeleteForm
from project.manager_frontend.utils.views import MultiFormView


class SavesListView(TemplateView):
    """
    Homepage view is actually only a "direct render to template"
    """
    template_name = "manager_frontend/rom_saves_list.html"
            
    def get_saves_list(self):
        keys = []
        saves_dict = defaultdict(list)
        
        # Walk through every files in saves directory
        for item in sorted(os.listdir(settings.RECALBOX_SAVES_PATH), key=keynat):
            filepath = os.path.join(settings.RECALBOX_SAVES_PATH, item)
            
            if os.path.isfile(filepath):
                filename = os.path.basename('.'.join(filepath.split('.')[0:-1]))
                ext = filepath.split('.')[-1]
                
                # Filter for only save disk (*.srm) and save states (*.state[0-9])
                if ext == 'srm' or ext.startswith('state'):
                    keys.append(item)
                    saves_dict[filename].append(item)
        
        # Order keys
        saves_dict = OrderedDict(sorted(saves_dict.items(), key=lambda t: t[0]))
        #print json.dumps(saves_dict.items(), indent=4)
        #print 
            
        return saves_dict.items()
            
    def get_context_data(self, **kwargs):
        context = super(SavesListView, self).get_context_data(**kwargs)
        context.update({
            'saves_list': self.get_saves_list(),
        })
        return context
