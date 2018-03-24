"""
Production Django Settings
"""
#
#   Imports
#
from .base import *
from .aws.conf import *


#
#   Additional Settings
#
DEBUG = False

ALLOWED_HOSTS = ['.douglasdaly.com']


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
