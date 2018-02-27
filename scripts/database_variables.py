# -*- coding: utf-8 -*-
"""
Script for setting DB Variables
"""
#
#   Imports
#
from script_helpers import process_input_dictionary


#
#   Variables
#

db_vars = {
    'DB_NAME': (None, False),
    'DB_USER': (None, False),
    'DB_PASSWORD': (None, True),
    'DB_HOST': (None, False),
    'DB_PORT': (5432, False)
}


#
#   Main Script
#
if __name__ == "__main__":
    process_input_dictionary(db_vars)
