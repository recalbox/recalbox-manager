"""
Assets tags

The assets map is a JSON file like this : ::

    {
        "stylesheets": {
            "css/recalbox.min.css": [
                "css/app.css"
            ]
        },
        "javascripts": {
            "js/modernizr.min.js": [
                "js/foundation5/vendor/modernizr.js"
            ],
        }
    }

This should be usable with grunt/gulp but without "glob" pattern.

Asset package key name must be the filepath to the package file and 
contain a list of asset file to package.

Note also that each path is relative to static directories, for 
gulp/grunt you would have to prepend them with the path to the project static dir (not 
the app static dirs, as they would not be reachable from Grung/Gulp)

This is only common static files usage, not for usage with static files through S3/etc..
"""
import json, os

from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.template.defaulttags import register
from django.contrib.staticfiles import finders

class AssetMapError(Exception):
    pass

class StaticfileAssetNotFound(Exception):
    pass


def render_asset_tags(kind, *bundle_names):
    """
    Helper to render asset tags using AssetTagsManager
    
    @kind: either 'stylesheets' or 'javascripts' (or whatever root element keys existing in the asset map)
    @bundle_names: list of bundles to get for the given kind name
    """
    # Open the template fragment
    tag_template = get_template(settings.ASSETS_TAG_TEMPLATES.get(kind))
    # Open and parse the JSON file for the map
    with open(settings.ASSETS_MAP_FILEPATH, 'rb') as json_file:
        assets_map = json.load(json_file)
    
    #print "* Kind:", kind
    manager = AssetTagsManager(assets_map[kind])
    #print
    
    return manager.render(bundle_names, tag_template)


@register.simple_tag
def stylesheet_tag(*bundle_names):
    """
    Build tag for stylesheet assets
    
    Usage
    *****
    
    Just gives package names (one or more) as arguments: ::
    
        {% stylesheet_tag "css/item1.min.css" "css/item2.min.css" .. %}
        
    Depending on settings.ASSETS_PACKAGED it would build (if True) an unique tag for the packaged asset file or (if False) tag for each package components files.
    """
    return render_asset_tags('stylesheets', *bundle_names)


@register.simple_tag
def javascript_tag(*bundle_names):
    """
    Build tag for javascript assets
    
    Usage
    *****
    
    Just gives package names (one or more) as arguments: ::
    
        {% javascript_tag "css/item1.min.js" "css/item2.min.js" .. %}
        
    Depending on settings.ASSETS_PACKAGED it would build (if True) an unique tag for the packaged asset file or (if False) tag for each package components files.
    """
    return render_asset_tags('javascripts', *bundle_names)


class AssetTagsManager(object):
    """
    Manage assets using given asset map
    
    This does not intend to compress/minify/uglify asset, just rendering their tags to 
    load them from your template
    
    @assets_map: file maps for an asset kind (not the full asset map)
    @packaged: switch to know if we use the packed files or the original ones
    """
    def __init__(self, assets_map, packaged=True):
        self.assets_map = assets_map # file maps for an asset kind (not the full asset map)
        self.packaged = packaged # switch to know if we use the packed files or the original ones
        
    def render_fragment(self, template, context=None):
        """
        Render fragment using given django template
        """
        return template.render(context)
    
    def static_url(self, filepath):
        """
        Have to raise a custom exception instead of output print
        
        Check if given relative file path exists in any static directory but 
        only is ASSETS_STRICT is enabled.
        
        Finally if there is not exception, return the static file url
        """
        if settings.ASSETS_STRICT:
            if not finders.find(filepath):
                raise StaticfileAssetNotFound("Asset file cannot be finded in any static directory: {}".format(filepath))
        return os.path.join(settings.STATIC_URL, filepath)
    
    def get_files(self, name):
        """
        Find and return asset file url given package name
        """
        try:
            file_paths = self.assets_map[name]
        except KeyError:
            if settings.ASSETS_STRICT:
                raise AssetMapError("Asset key '{}' does not exists in your asset map".format(name))
        else:
            if settings.ASSETS_PACKAGED:
                return [self.static_url(name)]
            else:
                return [self.static_url(item) for item in file_paths]
        return []
    
    def render(self, names, template):
        """
        Return rendered given template for each asset files of each package names
        """
        tags = []
        for name in names:
            asset_files = self.get_files(name)
            for item in filter(None, asset_files):
                tags.append( self.render_fragment(template, context=Context({"ASSET_URL": item})) )
            
        return '\n'.join(tags)
