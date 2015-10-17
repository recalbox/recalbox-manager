"""
Manifest parsers

The assets manifest is a JSON file like this : ::

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

This should be usable with grunt/gulp but without "glob" patterns.

Asset package key name must be the filepath to the package file and 
contain a list of asset file to package.

Note also that each path is relative to static directories, for 
gulp/grunt you would have to prepend them with the path to the project static dir (not 
the app static dirs, as they would not be reachable from Grung/Gulp)

This would eventually not work with static files through S3/etc..
"""
import os

from django.conf import settings
from django.template import Context
from django.template.loader import get_template as loader_get_template
from django.contrib.staticfiles import finders

class AssetMapError(Exception):
    pass


class StaticfileAssetNotFound(Exception):
    pass


class AssetTagsManagerBase(object):
    """
    Base for management assets using given asset map
    
    Just take assets map to get its files and render their HTML "loader" fragment
    
    This does not intend to compress/minify/uglify asset, just rendering their tags to 
    load them from your template
    
    @assets_map: file maps for an asset kind (not the full asset map)
    """
    def __init__(self, assets_map):
        self.assets_map = assets_map
        
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



class AssetTagsManagerFromManifest(AssetTagsManagerBase):
    """
    Override AssetTagsManagerBase to implement management from the whole 
    manifest
    """
    def __init__(self, manifest):
        self.manifest = manifest # full asset map from settings
        self.templates = self.get_templates()
        
    def get_templates(self):
        """
        Render fragment using given django template
        """
        templates = {}
        for k,v in settings.ASSETS_TAG_TEMPLATES.items():
            templates[k] = loader_get_template(v)
        return templates
    
    def render_for_kind(self, names, kind):
        self.assets_map = self.manifest[kind]
        return self.render(names, self.templates[kind])
