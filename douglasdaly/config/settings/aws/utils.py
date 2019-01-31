# -*- coding: utf-8 -*-
"""
config/settings/aws/utils.py

    Storages classes for S3 storage of Media and Static

"""
#
#   Imports
#
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


#
#   Storage Classes
#

class StaticRootS3BotoStorage(S3Boto3Storage):
    """
    Static Storages Class for S3 Boto3
    """
    location = settings.STATICFILES_LOCATION


class MediaRootS3BotoStorage(S3Boto3Storage):
    """
    Media Storages Class for S3 Boto3
    """
    location = settings.MEDIAFILES_LOCATION
