from django.conf.urls import url
from django.views.generic import TemplateView

from .views import HomeView
from .views.config import RecalboxConfigFormView
from .views.logs import LogsView
from .views.bios import BiosListView, BiosUploadJsonView
from .views.roms import RomListView, RomUploadJsonView
#from .views.saves import SavesListView
from .views.systems import SystemsListView
from .views.monitor import MonitoringView
from .views.moonlight import RecalboxMoonlightFormView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    
    url(r'^bios/$', BiosListView.as_view(), name='bios'),
    url(r'^bios/upload$', BiosUploadJsonView.as_view(), name='bios-upload'),
    
    url(r'^config/$', RecalboxConfigFormView.as_view(), name='config'),
    
    url(r'^monitoring/$', MonitoringView.as_view(), name='monitoring'),
    
    url(r'^logs/$', LogsView.as_view(), name='logs'),
    
    url(r'^systems/$', SystemsListView.as_view(), name='roms-systems'),

    url(r'^moonlight/$', RecalboxMoonlightFormView.as_view(), name='moonlight'),
    
    #url(r'^systems/roms/saves/$', SavesListView.as_view(), name='roms-saves-list'),
    
    url(r'^systems/roms/(?P<system>\w+)/$', RomListView.as_view(), name='roms-list'),
    url(r'^systems/roms/(?P<system>\w+)/upload/$', RomUploadJsonView.as_view(), name='roms-upload'),

]