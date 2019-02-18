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
from django.utils.translation import gettext_lazy as _

from colorful.widgets import ColorFieldWidget

from .widgets import ColorListFieldWidget, TextListFieldWidget
from .models import (
    Post, Category, Tag, BlogSettings, CustomJS, CustomCSS, ColorTheme,
    Author
)
from .utils import font_color_helper


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
#   Helper filters
#

class TagCategoryFilter(admin.SimpleListFilter):
    """
    Filter for Tag _category attribute
    """
    title = _('first letter')
    parameter_name = 'tag_letter'

    def lookups(self, request, model_admin):
        letters = set([t.get_category_from_name()
                       for t in model_admin.model.objects.all()])
        return [(l, l) for l in sorted(letters)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(_category=self.value())
        return queryset


#
#   Admin forms
#

class PostAdminForm(forms.ModelForm):
    """
    Admin form for blog posts
    """

    class Meta:
        widgets = {
            'description': forms.Textarea({'rows': 2}),
            'search_terms': TextListFieldWidget(),
        }


class ColorThemeAdminForm(forms.ModelForm):
    """
    Admin form for color themes
    """

    class Meta:
        model = ColorTheme
        fields = ('name', 'slug', 'colors')
        widgets = {
            'slug': forms.HiddenInput(),
            'colors': ColorListFieldWidget(),
        }


class HiddenSlugForm(forms.ModelForm):
    """
    Admin form hiding slug fields
    """

    class Meta:
        widgets = {
            'slug': forms.HiddenInput()
        }


class ThemedColorForm(forms.ModelForm):
    """
    Admin form for selecting colors from color theme
    """
    _color_fields = None

    def __init__(self, *args, **kwargs):
        super(ThemedColorForm, self).__init__(*args, **kwargs)

        if self._color_fields:
            blog_settings = BlogSettings.load()
            if blog_settings and blog_settings.color_theme:
                theme_colors = blog_settings.color_theme.colors
                for color_field in self._color_fields:
                    self.fields[color_field].widget = \
                        ColorFieldWidget(colors=theme_colors)


class TCAdminForm(ThemedColorForm):
    """
    Admin form for tags and categories
    """
    _color_fields = ('color',)

    class Meta:
        widgets = {
            'slug': forms.HiddenInput(),
            'search_terms': TextListFieldWidget(),
        }


#
#   Admin classes
#

@admin.register(BlogSettings)
class BlogSettingsAdmin(admin.ModelAdmin):
    """
    Admin class for blog settings
    """
    fieldsets = (
        (None, {
            'fields': ('title', 'site_link'),
        }),
        (_('General'), {
            'fields': ('show_authors', 'posts_per_page'),
        }),
        (_('Display'), {
            'fields': (
                'color_theme', 'code_style_sheet'
            ),
        }),
        (_('RSS Feeds'), {
            'fields': ('latest_feed_most_recent',),
        }),
    )

    def has_add_permission(self, request):
        """Override for singleton"""
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin for blog authors
    """
    fieldsets = (
        (None, {
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
    list_filter = ('is_active', 'show_posts')

    actions = ['make_active', 'make_inactive', 'make_show_posts',
               'make_unshow_posts']

    # - Display helpers

    def display_display_name(self, obj):
        """Get name to display helper"""
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


@admin.register(Post)
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
                'created', 'last_updated', 'publish_date'
            )
        }),
        (_('Description'), {
            'fields': (
                'icon_image', 'description', 'search_terms'
            )
        }),
        (_('Content'), {
            'fields': ('body',)
        }),
        (_('Additional Includes'), {
            'classes': ('collapse',),
            'fields': (
                'custom_javascript', 'css_includes', 'javascript_includes'
            ),
         }),
        (_('Actions'), {'fields': ('previewable', 'published',)}),
    )

    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created', 'last_updated')
    filter_horizontal = ('tags', 'css_includes', 'javascript_includes')

    search_fields = ('search_terms', 'description', 'title', 'tags', 'body')

    ordering = ('created',)
    date_hierarchy = 'publish_date'
    list_display = ('title', 'display_author', 'category', 'display_created',
                    'display_last_updated', 'previewable', 'published',
                    'display_display_date')
    list_filter = ('previewable', 'published', 'author', 'category', 'tags')

    actions = ['make_previewable', 'make_not_previewable', 'make_published',
               'make_not_published']

    # - Display Helpers

    def display_author(self, obj):
        """Display author helper"""
        if obj.author:
            return obj.author.get_display_name()
        return None
    display_author.short_description = 'Author'
    display_author.admin_order_field = 'author'

    def display_created(self, obj):
        """Display created date helper"""
        return obj.created.date()
    display_created.short_description = 'Created'
    display_created.admin_order_field = 'created'

    def display_last_updated(self, obj):
        """Display last_updated date helper"""
        return obj.last_updated.date()
    display_last_updated.short_description = 'Last Updated'
    display_last_updated.admin_order_field = 'last_updated'

    def display_display_date(self, obj):
        """Display display_date helper"""
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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin for blog categories
    """
    form = TCAdminForm

    fieldsets = (
        (None, {
            'fields': ('name', 'slug')
        }),
        (_('Display'), {
            'fields': ('description', 'icon_image', 'color')
        }),
        (_('Additional'), {
            'fields': ('search_terms',)
        }),
    )

    prepopulated_fields = {'slug': ('name',)}

    list_display = ('name', 'description')
    search_fields = ('name', 'description')

    # - Override to set font color

    def save_model(self, request, obj, form, change):
        """Override to set font color"""
        obj.font_color = font_color_helper(obj.color)
        super().save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin for blog tags
    """
    form = TCAdminForm

    fieldsets = (
        (None, {
            'fields': ('name', 'slug')
        }),
        (_('Display'), {
            'fields': ('description', 'icon_image', 'color')
        }),
        (_('Additional'), {
            'fields': ('search_terms',)
        }),
    )

    exclude = ('_category',)
    prepopulated_fields = {'slug': ('name',)}

    list_display = ('name', 'description')
    list_filter = (TagCategoryFilter,)
    search_fields = ('name', 'description')

    # - Override to set font color

    def save_model(self, request, obj, form, change):
        """Override to set font color"""
        obj.font_color = font_color_helper(obj.color)
        super().save_model(request, obj, form, change)


@admin.register(ColorTheme)
class ColorThemeAdmin(admin.ModelAdmin):
    """
    Admin for Color Themes
    """
    form = ColorThemeAdminForm

    fieldsets = (
        (None, {
            'fields': ('name', 'slug')
        }),
        (_('Colors'), {
            'fields': ('colors',)
        }),
    )

    prepopulated_fields = {'slug': ('name',)}


class CustomAdditionalAdmin(admin.ModelAdmin):
    """
    Admin for Custom JS and CSS objects
    """
    form = HiddenSlugForm

    fieldsets = (
        (None, {
            'fields': ('name', 'tag', 'slug', 'file')
        }),
    )

    prepopulated_fields = {'slug': ('tag', 'name')}

    list_display = ('name', 'tag')
    list_filter = ('tag',)


admin.site.register(CustomJS, CustomAdditionalAdmin)
admin.site.register(CustomCSS, CustomAdditionalAdmin)
