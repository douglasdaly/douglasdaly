# -*- coding: utf-8 -*-
"""
admin.py

    Admin modules for main site pages

@author: Douglas Daly
@date: 12/10/2017
"""
#
#   Imports
#
from django.contrib import admin

from .models import Page


#
#   Admin Classes
#

class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


#
#   Register Classes
#

admin.site.register(Page, PageAdmin)
