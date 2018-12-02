# -*- coding: utf-8 -*-
"""
AWS Config File
"""
#
#   Imports
#
import os
import datetime


# - AWS Stuff
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True
AWS_DEFAULT_ACL = None

DEFAULT_FILE_STORAGE = "config.settings.aws.utils.MediaRootS3BotoStorage"
STATICFILES_STORAGE = "config.settings.aws.utils.StaticRootS3BotoStorage"
AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
S3DIRECT_REGION = os.environ["S3DIRECT_REGION"]
AWS_S3_SIGNATURE_VERSION = 's3v4'
S3_URL = 'https://s3.{}.amazonaws.com/{}/'.format(S3DIRECT_REGION, AWS_STORAGE_BUCKET_NAME)
MEDIA_URL = S3_URL + 'media/'
STATIC_URL = S3_URL + 'static/'
MEDIA_ROOT = MEDIA_URL
ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = {
    'Expires': expires,
    'Cache-Control': 'max-age={0:n}'.format(int(two_months.total_seconds()))
}
