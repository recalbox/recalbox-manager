# -*- coding: utf-8 -*-
"""
Application Crumbs
"""
from autobreadcrumbs import site
from django.utils.translation import ugettext_lazy

site.update({
    'manager:home': ugettext_lazy('Home'),
    'manager:bios': ugettext_lazy('Bios'),
    'manager:config': ugettext_lazy('Configuration'),
    'manager:logs': ugettext_lazy('Logs'),
    'manager:roms-systems': ugettext_lazy('Rom systems'),
    'manager:roms-list': ugettext_lazy('Roms for "{{ system_name }}"'),
})
