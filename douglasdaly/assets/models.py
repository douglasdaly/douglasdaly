# -*- coding: utf-8 -*-
"""
Models for site assets

:author: Douglas Daly
:date: 1/5/2019
"""
#
#   Imports
#
from django.db import models
from django.core.exceptions import ValidationError

from sorl.thumbnail import ImageField


#
#   Models
#

class Asset(models.Model):
    """
    Base Asset class
    """
    title = models.CharField(max_length=120, unique=True)
    tag = models.CharField(max_length=80, null=True, default=None)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True, default=None)
    type = models.CharField(max_length=30, unique=False, null=False,
                            editable=False)

    # - Meta class and dunder methods

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def __unicode__(self):
        return "%s" % self.title


class ImageAsset(Asset):
    """
    Asset class for Image files
    """
    asset = ImageField(upload_to="assets/image/")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "image"


class FileAsset(Asset):
    """
    Asset class for Files
    """
    asset = models.FileField(upload_to="assets/file/")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "file"


class VideoAsset(Asset):
    """
    Asset class for Video files
    """
    asset = models.FileField(upload_to="assets/video/")
    video_width = models.SmallIntegerField(null=True, default=None)
    video_height = models.SmallIntegerField(null=True, default=None)
    autoplay = models.BooleanField(default=False)
    controls = models.BooleanField(default=True)
    loop = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "video"


# - Settings

class AssetSettings(models.Model):
    """
    Singleton settings class for Assets
    """
    default_video_width = models.SmallIntegerField(default=480)
    default_video_height = models.SmallIntegerField(default=360)
    default_video_autoplay = models.BooleanField(default=False)
    default_video_controls = models.BooleanField(default=True)

    # - Meta and dunder methods

    class Meta:
        verbose_name_plural = "Asset Settings"

    def __str__(self):
        return 'Asset Settings'

    def __unicode__(self):
        return self.__str__()

    # - Utility functions

    def save(self, *args, **kwargs):
        """Override to ensure only one instance exists"""
        if AssetSettings.objects.exists() and not self.pk:
            raise ValidationError('There can only be one instance of the Asset'
                                  ' Settings')
        else:
            return super(AssetSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Loads the Singleton Instance or returns None"""
        try:
            obj = cls.objects.get(pk=1)
        except cls.DoesNotExist:
            obj = None
        return obj
