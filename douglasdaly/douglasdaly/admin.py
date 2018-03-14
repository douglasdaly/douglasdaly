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
from adminsortable.admin import SortableAdmin

from .models import Page, SiteSettings, ImageAsset, FileAsset


#
#   Admin Classes
#

class PageAdmin(SortableAdmin):
    prepopulated_fields = {'slug': ('title',)}


class AssetAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


#
#   Register Classes
#

admin.site.register(Page, PageAdmin)
admin.site.register(SiteSettings)
admin.site.register(ImageAsset, AssetAdmin)
admin.site.register(FileAsset, AssetAdmin)
