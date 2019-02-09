# -*- coding: utf-8 -*-
"""
blog/admin.py

    Admin classes for blog application.

@author: Douglas Daly
@date: 2/8/2019
"""
#
#   Imports
#
from django import forms
from django.contrib import admin

from .models import Post, Category, Tag, BlogSettings, CustomJS, CustomCSS


#
#   Admin Classes
#

class PostAdminForm(forms.ModelForm):
    """Admin form for blog posts"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['rows'] = 2
        self.fields['body'].widget.attrs['rows'] = 25


class PostAdmin(admin.ModelAdmin):
    """Admin for blog posts"""
    form = PostAdminForm

    exclude = ('created', 'posted')
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'posted', 'published')
    list_filter = ('published', 'category')


class CategoryAdmin(admin.ModelAdmin):
    """Admin for blog categories"""
    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    """Admin for blog tags"""
    exclude = ('_category',)
    prepopulated_fields = {'slug': ('name',)}


#
#   Register Classes
#

admin.site.register(BlogSettings)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(CustomJS)
admin.site.register(CustomCSS)
