"""
Assets tags

TODO: another tag for loading asset kind that are not stylesheet or javascript
"""
from django.template.defaulttags import register

from project.assets_cartographer import manifest
from project.assets_cartographer.parser import AssetTagsManagerFromManifest

def render_asset_tags(kind, *bundle_names):
    """
    Shortcut to render asset tags using AssetTagsManagerFromManifest and 
    manifest registry
    
    @kind: either 'stylesheets' or 'javascripts' (or whatever root element keys existing in the asset map)
    @bundle_names: list of bundles to get for the given kind name
    """
    return AssetTagsManagerFromManifest(manifest.get_registry()).render_for_kind(bundle_names, kind)


@register.simple_tag
def asset_tag(kind, *bundle_names):
    """
    Build tag for any kind of asset
    
    Usage
    *****
    
    Give asset kind name as first argument, then package names (one or more) as other arguments: ::
    
        {% asset_tag "stylesheet" "css/item1.min.css" "css/item2.min.css" .. %}
        
    Depending on settings.ASSETS_PACKAGED it would build an unique tag (if True) for the packaged asset file or tag (if False) for each package components files.
    
    Obviously, the given kind have to exist in your asset manifest.
    """
    return render_asset_tags(kind, *bundle_names)


@register.simple_tag
def stylesheet_tag(*bundle_names):
    """
    Build tag for stylesheet assets
    
    Usage
    *****
    
    Just give package names (one or more) as arguments: ::
    
        {% stylesheet_tag "css/item1.min.css" "css/item2.min.css" .. %}
        
    Depending on settings.ASSETS_PACKAGED it would build an unique tag (if True) for the packaged asset file or tag (if False) for each package components files.
    """
    return render_asset_tags('stylesheets', *bundle_names)


@register.simple_tag
def javascript_tag(*bundle_names):
    """
    Build tag for javascript assets
    
    Usage
    *****
    
    Just give package names (one or more) as arguments: ::
    
        {% javascript_tag "css/item1.min.js" "css/item2.min.js" .. %}
        
    Depending on settings.ASSETS_PACKAGED it would build an unique tag (if True) for the packaged asset file or tag (if False) for each package components files.
    """
    return render_asset_tags('javascripts', *bundle_names)
