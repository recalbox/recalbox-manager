"""
Simple cartographer for assets, using a JSON manifest

Implement templatetags so defined assets in manifest can be loaded from a tag 
that switch to unpackaged or packaged version of asset files.

The app does not package itself the asset files, for this you can use something 
like grunt that would be able to load the JSON manifest to know what to package.

Have to load autodiscover() method (root urls.py should be a good choice) to load 
the manifest and fill registry.
"""
import os, json
from project.assets_cartographer.registry import manifest

def autodiscover():
    """
    Dummy loader actually, this should be backward compatible for futur assets 
    discovery per app
    """
    from django.conf import settings
    # Open and parse the JSON manifest
    with open(settings.ASSETS_MAP_FILEPATH, 'rb') as json_file:
        json_manifest = json.load(json_file)
    # Fill the registry with the whole JSON manifest    
    manifest.update(json_manifest)
