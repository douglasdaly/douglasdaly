# -*- coding: utf-8 -*-
"""
Admin classes for main site pages

:author: Douglas Daly
:date: 12/10/2017
"""
#
#   Imports
#
from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from adminsortable.admin import SortableAdmin

from .models import Page, SiteSettings, SiteAdminSettings


#
#   Admin site overrides
#

admin.site.site_header = "DouglasDaly.com Administration"
admin.site.site_title = "DouglasDaly.com Administration"


#
#   Model admin forms
#

class PageAdminForm(forms.ModelForm):
    """
    Admin form for main site pages
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['rows'] = 25


#
#   Model admin classes
#

@admin.register(Page)
class PageAdmin(SortableAdmin):
    """
    Admin for main site pages
    """
    form = PageAdminForm

    fieldsets = (
        (None, {
            'fields': ('title', 'slug')
        }),
        (_('Navigation'), {
            'fields': ('link_name', 'passthrough_page', 'passthrough_link'),
        }),
        (_('Content'), {
            'classes': ('wide',),
            'fields': ('content',),
        }),
        (_('Custom Extras'), {
            'classes': ('collapse',),
            'fields': ('custom_css', 'custom_javascript'),
        }),
        (_('Actions'), {
            'fields': ('published',),
        }),
    )

    prepopulated_fields = {'slug': ('title',)}


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    Admin class for main site singleton settings
    """
    fieldsets = (
        (None, {
            'fields': ('title',),
        }),
        (_('Meta Data'), {
            'fields': ('meta_author', 'meta_keywords', 'meta_description'),
        }),
        (_('Home Page Options'), {
            'fields': (
                'home_tagline', 'home_image', 'home_show_card',
                'number_recent_posts'
            ),
        }),
        (_('Site Analytics'), {
            'fields': ('google_analytics_key',),
        }),
        (_('Social Links'), {
            'fields': ('github_link', 'linkedin_link', 'twitter_link'),
        }),
    )

    def has_add_permission(self, request):
        """Override for singleton"""
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(SiteAdminSettings)
class SiteAdminSettingsAdmin(admin.ModelAdmin):
    """
    Admin class for main site admin singleton settings
    """
    fieldsets = (
        (_('System'), {
            'fields': (
                'site_is_active', 'inactive_page_title',
                'inactive_page_content'
            ),
        }),
        (_('404 Error Handling'), {
            'fields': ('err_404_title', 'err_404_content', 'err_404_sentry'),
        }),
        (_('500 Error Handling'), {
            'fields': ('err_500_title', 'err_500_content', 'err_500_sentry'),
        }),
    )

    def has_add_permission(self, request):
        """Override for singleton"""
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
