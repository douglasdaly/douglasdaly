# -*- coding: utf-8 -*-
"""
Admin site configuration overrides for main admin site.

:author: Douglas Daly
:date: 2/18/2019
"""
#
#   Imports
#
from django.contrib import admin


#
#   Admin site overrides
#

admin.site.site_header = "DouglasDaly.com Administration"
admin.site.site_title = "DouglasDaly.com Administration"
