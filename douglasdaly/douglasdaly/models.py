# -*- coding: utf-8 -*-
"""
models.py

    Models for the main site pages

@author: Douglas Daly
@date: 12/10/2017
"""
#
#   Imports
#
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator

from adminsortable.models import SortableMixin
from sorl.thumbnail import ImageField


#
#   Model Definitions
#

class SiteSettings(models.Model):
    title = models.CharField(max_length=20, unique=True)
    meta_description = models.CharField(max_length=120, null=True)
    meta_author = models.CharField(max_length=100, null=True)
    meta_keywords = models.CharField(max_length=120, null=True)

    number_recent_posts = models.PositiveSmallIntegerField(default=3,
                            blank=True, null=True,
                            verbose_name="Number of recent posts to show",
                            validators=[MaxValueValidator(3),])

    google_analytics_key = models.CharField(max_length=120, null=True,
                                            blank=True)

    github_link = models.URLField(null=True, blank=True)
    linkedin_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return 'Site Settings'

    def __unicode__(self):
        return self.__str__()

    def save(self, *args, **kwargs):
        """ Override to ensure only one instance exists
        """
        if SiteSettings.objects.exists() and not self.pk:
            raise ValidationError('There can only be one instance of the Site '
                                  'Settings')
        else:
            return super(SiteSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """ Loads the Singleton Instance or returns None
        """
        try:
            obj = cls.objects.get(pk=1)
        except cls.DoesNotExist:
            obj = None
        return obj


class SiteAdminSettings(models.Model):
    err_404_title = models.CharField(max_length=60, null=False,
                                     default="Page not Found (404)")
    err_404_content = models.TextField(null=True, blank=True, default=None)

    err_500_title = models.CharField(max_length=60, null=False,
                                     default="Server Error (500)")
    err_500_content = models.TextField(null=True, blank=True, default=None)

    default_video_width = models.SmallIntegerField(default=480)
    default_video_height = models.SmallIntegerField(default=360)
    default_video_autoplay = models.BooleanField(default=False)
    default_video_controls = models.BooleanField(default=True)

    def __str__(self):
        return 'Site Administration Settings'

    def __unicode__(self):
        return self.__str__()

    def save(self, *args, **kwargs):
        """ Override to ensure only one instance exists
        """
        if SiteAdminSettings.objects.exists() and not self.pk:
            raise ValidationError('There can only be one instance of the Site '
                                  'Administration Settings')
        else:
            return super(SiteAdminSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """ Loads the Singleton Instance or returns None
        """
        try:
            obj = cls.objects.get(pk=1)
        except cls.DoesNotExist:
            obj = None
        return obj


class Page(SortableMixin):
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

    class Meta:
        ordering = ['the_order']

    the_order = models.PositiveIntegerField(default=0, editable=False,
                                            db_index=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return "%s" % self.title

    def get_absolute_url(self):
        if not self.passthrough_page:
            return reverse('view_page', kwargs={'slug': self.slug})
        else:
            return self.passthrough_link


class Asset(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True, null=True, default=None)
    type = models.CharField(max_length=30, unique=False, null=False,
                            editable=False)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def __unicode__(self):
        return "%s" % self.title


class ImageAsset(Asset):
    asset = ImageField(upload_to="assets/image/")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "image"


class FileAsset(Asset):
    asset = models.FileField(upload_to="assets/file/")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "file"


class VideoAsset(Asset):
    asset = models.FileField(upload_to="assets/video/")
    video_width = models.SmallIntegerField(null=True, default=None)
    video_height = models.SmallIntegerField(null=True, default=None)
    autoplay = models.BooleanField(default=False)
    controls = models.BooleanField(default=True)
    loop = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "video"
