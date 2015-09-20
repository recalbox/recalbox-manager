"""recalbox-manager URL Configuration for development environment

Inherit from the default 'urls.py'
"""
from .urls import *

# Debug
#if settings.DEBUG:
urlpatterns = patterns('',
    (r'^icomoon/', include('icomoon.urls', namespace='icomoon')),
) + urlpatterns
