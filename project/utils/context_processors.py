# -*- coding: utf-8 -*-
import imp, os, socket
from django.conf import settings

def get_host_ipaddress():
    """
    Little trick to get all host ip address
    
    Stealed from http://stackoverflow.com/a/1267524/4884485
    
    Return a string with host ip address
    """
    return [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

def get_site_metas(with_static=False, with_media=False, is_secure=False,
                   extra={}):
    """
    Return metas from the current *Site* and settings

    Added Site metas will be callable in templates like this
    ``SITE.themetaname``

    This can be used in code out of a Django requests (like in management
    commands) or in a context processor to get the *Site* urls.

    Default metas returned :

    * SITE.name: Current *Site* entry name;
    * SITE.domain: Current *Site* entry domain;
    * SITE.web_url: The Current *Site* entry domain prefixed with the http
      protocol like ``http://mydomain.com``. If HTTPS is enabled 'https' will be used instead of 'http';
    * SITE.hostname: The current hostname, like ``SITE.domain`` but without port if any;

    Optionally it can also return ``STATIC_URL`` and ``MEDIA_URL`` if needed
    (like out of Django requests).
    """
    # Dont use Site framework, instead use the setted infos and use a trick to 
    # find the ip adress if the ip is not fixed
    if getattr(settings, 'SITE_FIXED', ''):
        site_current = getattr(settings, 'SITE_FIXED')
        
        host_address = [site_current.get('ip', None) or get_host_ipaddress()]
        
        if site_current.get('port', None):
            host_address.append(site_current.get('port'))
        
        metas = {
            'SITE': {
                'name': site_current.get('name', ''),
                'domain': ':'.join(host_address),
                'hostname': host_address[0],
            }
        }
        metas['SITE']['web_url'] = 'http://%s' % metas['SITE']['domain']
    # Fallback and use the Site framework
    else:
        from django.contrib.sites.models import Site
        site_current = Site.objects.get_current()
        metas = {
            'SITE': {
                'name': site_current.name,
                'domain': site_current.domain,
                'hostname': site_current.domain.split(':')[0],
                'web_url': 'http://%s' % site_current.domain,
            }
        }
            
    if is_secure:
        metas['web_url'] = 'https://%s' % site_current.domain
    if with_media:
        metas['MEDIA_URL'] = getattr(settings, 'MEDIA_URL', '')
    if with_static:
        metas['STATIC_URL'] = getattr(settings, 'STATIC_URL', '')
    metas.update(extra)
    return metas


def manager_version(request):
    """
    Context processor to add the recalbox-manager version
    """
    # Tricky way to know the manager version because its version lives out of project path
    root = imp.load_source('__init__', os.path.join(settings.BASE_DIR, '__init__.py'))
    return {'manager_version': root.__version__}

def site_metas(request):
    """
    Context processor to add the current *Site* metas to the context
    """
    return get_site_metas(is_secure=request.is_secure())
