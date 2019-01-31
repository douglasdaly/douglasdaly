# -*- coding: utf-8 -*-
"""
AWS Config File
"""
#
#   Imports
#
import os


# - AWS Stuff
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
AWS_DEFAULT_ACL = None
AWS_BUCKET_ACL = None
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_S3_REGION_NAME = os.environ["AWS_S3_REGION_NAME"]
AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)


# - File storage settings
MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = "config.settings.aws.utils.MediaRootS3BotoStorage"

STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = "config.settings.aws.utils.StaticRootS3BotoStorage"

MEDIA_URL = 'https://{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
STATIC_URL = 'https://{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
