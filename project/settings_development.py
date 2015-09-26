from .settings import *

INSTALLED_APPS = tuple(list(INSTALLED_APPS)+[
    'debug_toolbar',
    'icomoon',
])

# For Django Debug Toolbar
INTERNAL_IPS = ('192.168.0.112',)

# For django-icomoon
ICOMOON_MANIFEST_FILEPATH = os.path.join(PROJECT_DIR, 'webapp_statics/fonts/selection.json')

ICOMOON_PRIVATE = False


ROOT_URLCONF = 'project.urls_development'
