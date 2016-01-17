"""recalbox-manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

# Discover crumbs from enabled apps
import autobreadcrumbs
autobreadcrumbs.autodiscover()

# Load asset manifest in memory
from project import assets_cartographer
assets_cartographer.autodiscover()

# Load Recalbox manifest in memory
from project import recalbox_manifest
recalbox_manifest.autodiscover()

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('project.manager_frontend.urls', namespace='manager')),
    #url(r'^api/', include('project.api.urls', namespace='api')),
]

# Debug
#if settings.DEBUG:
urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^500/$', TemplateView.as_view(template_name="500.html")),
    url(r'^404/$', TemplateView.as_view(template_name="404.html")),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns
