from django.conf.urls import url
from django.views.generic import TemplateView

from .views import HomeView
from .views.config import RecalboxConfigFormView
from .views.logs import LogsView
from .views.bios import BiosListView
from .views.roms import SystemsListView, RomListView, RomUploadJsonView
from .views.monitor import MonitoringView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    
    url(r'^bios/$', BiosListView.as_view(), name='bios'),
    
    url(r'^config/$', RecalboxConfigFormView.as_view(), name='config'),
    
    url(r'^monitoring/$', MonitoringView.as_view(), name='monitoring'),
    
    url(r'^logs/$', LogsView.as_view(), name='logs'),
    
    url(r'^systems/$', SystemsListView.as_view(), name='roms-systems'),
    url(r'^systems/roms/(?P<system>\w+)/$', RomListView.as_view(), name='roms-list'),
    url(r'^systems/roms/(?P<system>\w+)/upload/$', RomUploadJsonView.as_view(), name='roms-upload'),
]