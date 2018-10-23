"""
Local Debug Django Settings
"""
#
#   Imports
#
from .local import *


#
#   Additional Settings
#

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Debug Toolbar

INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']