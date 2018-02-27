# -*- coding: utf-8 -*-
"""
Script for setting AWS Variables
"""
#
#   Imports
#
from script_helpers import process_input_dictionary


#
#   Variables
#

aws_vars = {
    'AWS_ACCESS_KEY_ID': (None, False),
    'AWS_SECRET_ACCESS_KEY': (None, True),
    'AWS_STORAGE_BUCKET_NAME': (None, False),
    'S3DIRECT_REGION': ('us-east-2', False)
}


#
#   Main Script
#
if __name__ == "__main__":
    process_input_dictionary(aws_vars)
