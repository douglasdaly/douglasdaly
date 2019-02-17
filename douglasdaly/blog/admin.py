# -*- coding: utf-8 -*-
"""
Admin classes for blog application.

:author: Douglas Daly
:date: 2/8/2019
"""
#
#   Imports
#
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _

from .widgets import DataAttributeSelectWidget
from .models import (
    Post, Category, Tag, BlogSettings, CustomJS, CustomCSS, ColorTheme,
    ColorThemeColor, Author
)


#
#   Admin forms
#

class PostAdminForm(forms.ModelForm):
    """
    Admin form for blog posts
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['description'].widget.attrs['rows'] = 2
        self.fields['search_terms'].widget.attrs['rows'] = 1
        self.fields['body'].widget.attrs['style'] = 'width: 100%'

        self.fields['tags'].widget = FilteredSelectMultiple(
            'Tags', False,
            choices=[(tag.id, str(tag)) for tag in Tag.objects.all()]
        )
        self.fields['css_includes'].widget = FilteredSelectMultiple(
            'CSS Includes', False,
            choices=[(css.id, str(css)) for css in CustomCSS.objects.all()]
        )
        self.fields['javascript_includes'].widget = FilteredSelectMultiple(
            'Javscript Includes', False,
            choices=[(js.id, str(js)) for js in CustomJS.objects.all()]
        )


class ColorThemeAdminForm(forms.ModelForm):
    """
    Admin form for Color Themes
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        data = {
            'style': {'': ''}
        }
        for c in ColorThemeColor.objects.all():
            data['style'][c.id] = "background-color: {}".format(c.color)

        self.fields['colors'].widget = DataAttributeSelectWidget(
            choices=[(c.id, str(c)) for c in ColorThemeColor.objects.all()],
            allow_multiple_selected=True,
            data=data
        )


#
#   Helper functions
#

def _action_property_helper(queryset, **kwargs):
    """Helper function for updating properties on given items"""
    return queryset.update(**kwargs)


def _action_message_helper(obj_cls, n_updated, message=None,
                           force_plural=False):
    """Helper function for getting notification messages after actions"""
    if n_updated == 1 and not force_plural:
        ret = "1 %s " % obj_cls._meta.verbose_name.title()
    else:
        ret = "%s %s " % (n_updated, obj_cls._meta.verbose_name_plural.title())

    if not message:
        message = "was updated successfully."

    if not message.endswith('.'):
        message = "%s." % message

    return "%s %s" % (ret, message)


#
#   Admin classes
#

class BlogSettingsAdmin(admin.ModelAdmin):
    """
    Admin class for blog settings
    """
    fieldsets = (
        (_('Information'), {
            'fields': ('title', 'site_link'),
        }),
        (_('Display Settings'), {
            'fields': (
                'posts_per_page', 'latest_feed_most_recent', 'show_authors',
                'color_theme', 'code_style_sheet'
            ),
        }),
    )


class AuthorAdmin(admin.ModelAdmin):
    """
    Admin for blog authors
    """
    fieldsets = (
        (_('Information'), {
            'fields': (
                'first_name', 'last_name', 'display_name'
            )
        }),
        (_('System'), {'fields': ('user', 'slug')}),
        (_('Description'), {
            'fields': ('author_image', 'author_bio', 'author_website')
        }),
        (_('Contact Information'), {
            'fields': (
                'contact_email', 'public_contact_email', 'display_public_email'
            )
        }),
        (_('Actions'), {'fields': ('is_active', 'show_posts',)}),
    )

    prepopulated_fields = {'slug': ('last_name', 'first_name', 'display_name')}

    search_fields = ('last_name', 'first_name', 'display_name')

    list_display = ('display_display_name', 'first_name', 'last_name',
                    'contact_email', 'is_active', 'show_posts')
    list_filter = ('is_active', 'show_posts',)

    actions = ['make_active', 'make_inactive', 'make_show_posts',
               'make_unshow_posts']

    # - Display helpers

    def display_display_name(self, obj):
        return obj.get_display_name()
    display_display_name.short_description = 'Display Name'
    display_display_name.admin_order_field = 'first_name'

    # - Actions

    def make_inactive(self, request, queryset):
        """Make the selected authors inactive"""
        rows_updated = _action_property_helper(queryset, is_active=False)
        msg = _action_message_helper(Author, rows_updated)
        self.message_user(request, msg)

    make_inactive.short_description = "Mark selected authors as inactive"

    def make_active(self, request, queryset):
        """Make selected authors active"""
        rows_updated = _action_property_helper(queryset, is_active=True)
        msg = _action_message_helper(Author, rows_updated)
        self.message_user(request, msg)

    make_active.short_description = "Mark selected authors as active"

    def make_show_posts(self, request, queryset):
        """Make selected authors' posts show"""
        rows_updated = _action_property_helper(queryset, show_posts=True)
        msg = _action_message_helper(Author, rows_updated)
        self.message_user(request, msg)

    make_show_posts.short_description = "Show posts from selected authors"

    def make_unshow_posts(self, request, queryset):
        """Make selected authors' posts not show"""
        rows_updated = _action_property_helper(queryset, show_posts=False)
        msg = _action_message_helper(Author, rows_updated)
        self.message_user(request, msg)

    make_unshow_posts.short_description = \
        "Do not show posts from selected authors"


class PostAdmin(admin.ModelAdmin):
    """
    Admin for blog posts
    """
    form = PostAdminForm

    fieldsets = (
        (None, {'fields': ('title', 'slug', 'author')}),
        (_('Classification'), {'fields': ('category', 'tags')}),
        (_('Meta Data'), {
            'fields': (
                'publish_date', 'icon_image', 'description', 'search_terms'
            )
        }),
        (_('Content'), {
            'fields': ('body',)
        }),
        (_('Additional Includes'),
         {
             'fields': (
                 'custom_javascript', 'css_includes', 'javascript_includes'
             )
         }),
        (_('Actions'), {'fields': ('previewable', 'published',)}),
    )

    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags', 'css_includes', 'javascript_includes')

    search_fields = ('search_terms', 'description', 'title', 'tags', 'body')

    list_display = ('title', 'display_author', 'category', 'display_created',
                    'display_last_updated', 'previewable', 'published',
                    'display_display_date')
    list_filter = ('previewable', 'published', 'author', 'category', 'tags')

    actions = ['make_previewable', 'make_not_previewable', 'make_published',
               'make_not_published']

    # - Display Helpers

    def display_author(self, obj):
        if obj.author:
            return obj.author.get_display_name()
        return None
    display_author.short_description = 'Author'
    display_author.admin_order_field = 'author'

    def display_created(self, obj):
        return obj.created.date()
    display_created.short_description = 'Created'
    display_created.admin_order_field = 'created'

    def display_last_updated(self, obj):
        return obj.last_updated.date()
    display_last_updated.short_description = 'Last Updated'
    display_last_updated.admin_order_field = 'last_updated'

    def display_display_date(self, obj):
        if obj.publish_date:
            return obj.display_date.date()
        return None
    display_display_date.short_description = 'Display Date'
    display_display_date.admin_order_field = 'display_date'

    # - Actions

    def make_previewable(self, request, queryset):
        """Make the selected post(s) previewable"""
        n_updated = _action_property_helper(queryset, previewable=True)
        msg = _action_message_helper(Post, n_updated,
                                     message="are now previewable")
        self.message_user(request, msg)
    make_previewable.short_description = \
        "Make the selected post(s) previewable"

    def make_not_previewable(self, request, queryset):
        """Make the selected post(s) not-previewable"""
        n_updated = _action_property_helper(queryset, previewable=False)
        msg = _action_message_helper(Post, n_updated,
                                     message="are no longer previewable")
        self.message_user(request, msg)
    make_not_previewable.short_description = \
        "Make the selected post(s) not-previewable"

    def make_published(self, request, queryset):
        """Make the selected post(s) published"""
        n_updated = _action_property_helper(queryset, published=True)
        msg = _action_message_helper(Post, n_updated,
                                     message="are now published")
        self.message_user(request, msg)
    make_published.short_description = "Publish the selected post(s)"

    def make_not_published(self, request, queryset):
        """Make the selected post(s) not published"""
        n_updated = _action_property_helper(queryset, published=False)
        msg = _action_message_helper(Post, n_updated,
                                     message="are no longer published")
        self.message_user(request, msg)
    make_not_published.short_description = "Un-publish the selected post(s)"


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin for blog categories
    """
    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    """
    Admin for blog tags
    """
    exclude = ('_category',)
    prepopulated_fields = {'slug': ('name',)}


class ColorThemeAdmin(admin.ModelAdmin):
    """
    Admin for Color Themes
    """
    form = ColorThemeAdminForm

    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('colors',)


#
#   Register Classes
#

admin.site.register(Author, AuthorAdmin)
admin.site.register(ColorThemeColor)
admin.site.register(ColorTheme, ColorThemeAdmin)
admin.site.register(BlogSettings, BlogSettingsAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(CustomJS)
admin.site.register(CustomCSS)
