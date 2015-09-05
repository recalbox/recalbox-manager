from .settings import *

INSTALLED_APPS = tuple(list(INSTALLED_APPS)+[
    'debug_toolbar',
])

# For Django Debug Toolbar
INTERNAL_IPS = ('192.168.0.112',)
