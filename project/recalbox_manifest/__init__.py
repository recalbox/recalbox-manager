"""
Recalbox manifest to know everything about supported systems
"""
import os, json
from .registry import manifest

def autodiscover():
    """
    Simple manifest loader
    """
    from django.conf import settings
    from .parser import RecalboxManifestParser
    # Fill the registry with the whole JSON manifest    
    manifest.update(
        RecalboxManifestParser(settings.RECALBOX_MANIFEST_FILEPATH).read()
    )
