# -*- coding: utf-8 -*-
import warnings

from importlib import import_module

def safe_import_module(path, default=None):
    """
    Try to import the specified module from the given Python path
    
    @path is a string containing a Python path to the wanted module, @default is 
    an object to return if import fails, it can be None, a callable or whatever you need.
    
    Return a object or None
    """
    if path is None:
        return default
    
    dot = path.rindex('.')
    module_name = path[:dot]
    class_name = path[dot + 1:]
    try:
        _class = getattr(import_module(module_name), class_name)
        return _class
    except (ImportError, AttributeError):
        warnings.warn('%s cannot be imported' % path, RuntimeWarning)
    return default
