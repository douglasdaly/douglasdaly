# -*- coding: utf-8 -*-
"""
Models for the main site.

:author: Douglas Daly
:date: 12/10/2017
"""
#
#   Imports
#
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator

from adminsortable.models import SortableMixin

from assets.models import ImageAsset


#
#   Model Definitions
#

# - Settings

class SiteSettings(models.Model):
    """
    Site settings singleton model
    """
    title = models.CharField(max_length=20, unique=True)
    meta_description = models.CharField(max_length=120, null=True)
    meta_author = models.CharField(max_length=100, null=True)
    meta_keywords = models.CharField(max_length=120, null=True)

    home_show_card = models.BooleanField(default=True, null=False)
    home_tagline = models.TextField(null=True, default=None, blank=True)
    home_image = models.ForeignKey(ImageAsset, default=None, blank=True,
                                   null=True, on_delete=models.SET_NULL)

    number_recent_posts = models.PositiveSmallIntegerField(
        default=3, blank=True, null=True,
        verbose_name="Number of recent posts to show",
        validators=[MaxValueValidator(3)]
    )

    google_analytics_key = models.CharField(max_length=120, null=True,
                                            blank=True)

    github_link = models.URLField(null=True, blank=True)
    linkedin_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)

    # - Meta and dunder methods

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'Site Settings'

    def __unicode__(self):
        return self.__str__()

    # - Singleton overrides

    def save(self, *args, **kwargs):
        """Override to ensure only one instance exists"""
        if SiteSettings.objects.exists() and not self.pk:
            raise ValidationError('There can only be one instance of the Site '
                                  'Settings')
        else:
            return super(SiteSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Loads the Singleton Instance or returns None"""
        try:
            obj = cls.objects.get(pk=1)
        except cls.DoesNotExist:
            obj = None
        return obj


class SiteAdminSettings(models.Model):
    """
    Site administration singleton settings model
    """
    site_is_active = models.BooleanField(default=True, null=False)
    inactive_page_title = models.CharField(max_length=80, null=True,
                                           default="Undergoing Maintenance")
    inactive_page_content = models.TextField(null=True, blank=True,
                                             default=None)

    err_404_title = models.CharField(max_length=80, null=False,
                                     default="Page not Found (404)")
    err_404_content = models.TextField(null=True, blank=True, default=None)
    err_404_sentry = models.BooleanField(default=False)

    err_500_title = models.CharField(max_length=80, null=False,
                                     default="Server Error (500)")
    err_500_content = models.TextField(null=True, blank=True, default=None)
    err_500_sentry = models.BooleanField(default=True)

    # - Meta class and dunder methods

    class Meta:
        verbose_name = "Site Admin Settings"
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'Site Administration Settings'

    def __unicode__(self):
        return self.__str__()

    # - Singleton overrides

    def save(self, *args, **kwargs):
        """Override to ensure only one instance exists"""
        if SiteAdminSettings.objects.exists() and not self.pk:
            raise ValidationError('There can only be one instance of the Site '
                                  'Administration Settings')
        else:
            return super(SiteAdminSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Loads the Singleton Instance or returns None"""
        try:
            obj = cls.objects.get(pk=1)
        except cls.DoesNotExist:
            obj = None
        return obj


# - Content

class Page(SortableMixin):
    """
    Main site page model
    """
    title = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    link_name = models.CharField(max_length=40, unique=True)
    keywords = models.CharField(max_length=120, null=True, default=None,
                                blank=True)
    passthrough_page = models.BooleanField(default=False)
    passthrough_link = models.CharField(max_length=40, default=None, null=True,
                                        blank=True)
    custom_css = models.FileField(upload_to="style/", default=None, null=True,
                                  blank=True)
    custom_javascript = models.FileField(upload_to="scripts/", default=None,
                                         null=True, blank=True)
    content = models.TextField(default=None, null=True, blank=True)

    published = models.BooleanField(default=True, null=False)

    # - Meta class and dunder methods

    class Meta:
        ordering = ['the_order']

    the_order = models.PositiveIntegerField(default=0, editable=False,
                                            db_index=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return "%s" % self.title

    # - Utility methods

    def get_absolute_url(self):
        if not self.passthrough_page:
            return reverse('view_page', kwargs={'slug': self.slug})
        else:
            return self.passthrough_link
