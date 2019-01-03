# -*- coding: utf-8 -*-
"""
config/settings/sentry_setup.py

    Setup for Sentry.io integration

@author: Douglas Daly
@date: 1/2/2019
"""
#
#   Imports
#
import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


#
#   Sentry Initialization
#

def initialize_sentry(environment):
    """Function to initialize Sentry"""
    if "SENTRY_DSN" in os.environ.keys():
        sentry_sdk.init(
            dsn=os.environ.get("SENTRY_DSN"),
            environment=environment,
            integrations=[DjangoIntegration()]
        )
        return True
    return False
