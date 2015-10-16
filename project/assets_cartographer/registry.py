# -*- coding: utf-8 -*-
"""
Asset manifest registry
"""
class AlreadyRegistered(Exception):
    pass

class NotRegistered(Exception):
    pass

class AssetManifestRegistry(object):
    """
    Manifest registry interface to store manifest entries
    """
    def __init__(self):
        self._registry = {} # title_key (string) -> title_name (string)
        self.global_context = None

    def get_registry(self):
        return self._registry

    def has_title(self, key):
        return key in self._registry

    def register(self, key, name):
        """
        Register a title key
        
        Raise ``AlreadyRegistered`` if the key is allready registered
        
        :type key: string
        :param key: the title key to add
        
        :type name: string
        :param name: title name
        """
        if self.has_title(key):
            raise AlreadyRegistered('Asset kind key "%s" is already registered' % key)
        # Instantiate the admin class to save in the registry
        self._registry[key] = name

    def unregister(self, key):
        """
        Unregister a title key
        
        Raise ``NotRegistered`` if the key is not registered
        
        :type key: string
        :param key: the title key to remove
        """
        if not self.has_title(key):
            raise NotRegistered('Asset kind key "%s" is not registered' % key)
        del self._registry[key]

    def update(self, names):
        """
        Update registry
        
        :type names: dict
        :param key: Titles dict (key -> name)
        """
        self._registry.update(names)

# Default breadcrumbs site
manifest = AssetManifestRegistry()
