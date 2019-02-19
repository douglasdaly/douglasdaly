# -*- coding: utf-8 -*-
"""
Admin classes and forms for Assets application.

:author: Douglas Daly
:date: 1/5/2019
"""
#
#   Imports
#
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.contrib import admin, messages
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _

from .models import ImageAsset, FileAsset, VideoAsset, AssetSettings
from .forms import BulkUploadForm


#
#   Admin forms
#


#
#   Admin classes
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
    change_list_template = "admin/assets/asset_change_list.html"

    fieldsets = (
        (_('Description'), {
            'fields': ('title', 'tag', 'slug', 'description')
        }),
    )

    prepopulated_fields = {'slug': ('tag', 'title',)}

    list_display = ('title', 'tag', 'slug')
    list_filter = ('tag',)
    ordering = ('tag', 'title')

    search_fields = ('title', 'description', 'tag')

    def get_urls(self):
        """Override for bulk upload functions"""
        urls = super().get_urls()
        addl_urls = [
            path(
                'bulk_asset_upload/',
                self.admin_site.admin_view(self.bulk_asset_upload),
            ),
        ]
        return addl_urls + urls

    # - Custom views for actions

    def bulk_asset_upload(self, request):
        """View for bulk asset upload form"""
        if request.method != 'POST':
            form = BulkUploadForm()

        else:
            form = BulkUploadForm(request.POST, request.FILES)

            if form.is_valid():
                try:
                    adds, replacements, errors = form.save()
                except Exception as ex:
                    pass
                else:
                    if len(adds) + len(replacements) > 0:
                        info_str = 'Success: '
                        if len(adds) > 0:
                            info_str = '%s %s assets added,' % (
                                info_str, len(adds)
                            )
                        if len(replacements) > 0:
                            info_str = '%s %s assets replaced' % (
                                info_str, len(replacements)
                            )
                        self.message_user(request, info_str.strip(','))

                    if len(errors) > 0:
                        error_to_file = dict()
                        for k, v in errors.items():
                            if v['error'] not in error_to_file.keys():
                                error_to_file[v['error']] = list()
                            error_to_file[v['error']].append(k)

                        for error_type, files in error_to_file.items():
                            error_str = "%s errors occurred: %s" % (
                                len(files), error_type
                            )
                            self.message_user(request, error_str,
                                              messages.ERROR)
                    url = reverse('admin:assets_%s_changelist' %
                                  self.model._meta.model_name)
                    return HttpResponseRedirect(url)

        # - Get context and render form
        context = self.admin_site.each_context(request)

        context['opts'] = self.model._meta
        context['form'] = form
        context['description'] = form.Meta.description

        return TemplateResponse(
            request,
            "admin/assets/bulk_asset_upload.html",
            context,
        )


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

