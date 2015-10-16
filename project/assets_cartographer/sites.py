# -*- coding: utf-8 -*-
"""
Manifest registry for assets
"""
class AlreadyRegistered(Exception):
    pass

class NotRegistered(Exception):
    pass

class AssetManifest(object):
    """
    Site registry interface
    """
    def __init__(self):
        self._registry = {} # title_key (string) -> title_name (string)
        self.global_context = None

    def get_registry(self):
        return self._registry

    def set_context(self, **kwargs):
        """
        Définit un contexte de base identique pour toute les instances de contrôleur
        """
        self.global_context = kwargs

    def has_title(self, key):
        return key in self._registry

    def get_title(self, key):
        """
        Get the internationalized title if i18n is used
        
        :type key: string
        :param key: title key
        
        :rtype: string
        :return: the translated title
        """
        if not self.has_title(key):
            raise NotRegistered('The title key "%s" is not registered' % key)
        return self._registry[key]

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
            raise AlreadyRegistered('The title key "%s" is already registered' % key)
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
            raise NotRegistered('The title key "%s" is not registered' % key)
        del self._registry[key]

    def update(self, names):
        """
        Update the registry with many titles
        
        :type names: dict
        :param key: Titles dict (key -> name)
        """
        self._registry.update(names)

# Default asset manifest
manifest = AssetManifest()
