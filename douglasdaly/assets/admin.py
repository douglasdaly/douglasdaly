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
from django.utils.translation import gettext_lazy as _

from .models import ImageAsset, FileAsset, VideoAsset, AssetSettings


#
#   Admin Classes
#

@admin.register(AssetSettings)
class AssetSettingsAdmin(admin.ModelAdmin):
    """
    Admin class for AssetSettings object
    """
    fieldsets = (
        (_("Video"), {
            'fields': (
                'default_video_width', 'default_video_height',
                'default_video_autoplay', 'default_video_controls'
            )
        }),
    )

    def has_add_permission(self, request):
        """Override for singleton"""
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


class BaseAssetAdmin(admin.ModelAdmin):
    """
    Base admin class for Assets
    """
    fieldsets = (
        (_('Description'), {
            'fields': ('title', 'tag', 'slug', 'description')
        }),
    )

    prepopulated_fields = {'slug': ('tag', 'title',)}

    list_display = ('title', 'tag')
    list_filter = ('tag',)

    search_fields = ('title', 'description', 'tag')


class AssetAdmin(BaseAssetAdmin):
    """
    Generic admin class for assets
    """
    fieldsets = (
        *BaseAssetAdmin.fieldsets,
        (_('Data'), {
            'fields': ('asset',)
        }),
    )


@admin.register(VideoAsset)
class VideoAssetAdmin(BaseAssetAdmin):
    """
    Admin class for Video Assets
    """
    fieldsets = (
        *BaseAssetAdmin.fieldsets,
        (_('Data'), {
            'fields': ('asset', 'video_width', 'video_height',)
        }),
        (_('Video'), {
            'fields': ('autoplay', 'controls', 'loop')
        }),
    )


# - Register remaining models

admin.site.register(ImageAsset, AssetAdmin)
admin.site.register(FileAsset, AssetAdmin)

