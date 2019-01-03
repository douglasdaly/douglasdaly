# -*- coding: utf-8 -*-
"""
config/settings/local.py

    Local Non-Debug Django Settings

@author: Douglas Daly
@date: 1/2/2019
"""
#
#   Imports
#
from .base import *


#
#   Additional Settings
#

# Hosts
ALLOWED_HOSTS = ['*']

# Debug Toolbar

INTERNAL_IPS = ['127.0.0.1']

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
