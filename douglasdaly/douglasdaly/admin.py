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

from adminsortable.admin import SortableAdmin

from .models import Page, SiteSettings, SiteAdminSettings


#
#   Model admin classes
#

class PageAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['rows'] = 25


class PageAdmin(SortableAdmin):
    form = PageAdminForm

    prepopulated_fields = {'slug': ('title',)}


#
#   Register Classes
#

admin.site.register(Page, PageAdmin)
admin.site.register(SiteSettings)
admin.site.register(SiteAdminSettings)
