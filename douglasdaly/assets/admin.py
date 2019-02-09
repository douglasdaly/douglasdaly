# -*- coding: utf-8 -*-
"""
assets/admin.py

    Admin registration of Asset models

@author: Douglas Daly
@date: 1/5/2019
"""
#
#   Imports
#
from django.contrib import admin

from .models import ImageAsset, FileAsset, VideoAsset, AssetSettings


#
#   Admin Classes
#

class AssetAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('tag', 'title',)}


# Register your models here.

admin.site.register(ImageAsset, AssetAdmin)
admin.site.register(FileAsset, AssetAdmin)
admin.site.register(VideoAsset, AssetAdmin)
admin.site.register(AssetSettings)
