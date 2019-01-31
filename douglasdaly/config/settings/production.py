# -*- coding: utf-8 -*-
"""
Production Django Settings
"""
#
#   Imports
#
from .base import *
from .aws.conf import *
from .sentry_setup import initialize_sentry


#
#   Additional Settings
#

initialize_sentry(os.environ.get("SENTRY_ENV", "production"))

DEBUG = False

ALLOWED_HOSTS = ['www.douglasdaly.com']

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST': os.environ.get("DB_HOST"),
        'PORT': os.environ.get("DB_PORT"),
    }
}

INSTALLED_APPS += ['storages']
