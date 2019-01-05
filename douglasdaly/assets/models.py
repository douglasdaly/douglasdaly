# -*- coding: utf-8 -*-
"""
douglasdaly/assets/models.py

    Models for site assets

@author: Douglas Daly
@date: 1/5/2019
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

# - Assets

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


# - Settings

class AssetSettings(models.Model):
    default_video_width = models.SmallIntegerField(default=480)
    default_video_height = models.SmallIntegerField(default=360)
    default_video_autoplay = models.BooleanField(default=False)
    default_video_controls = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Asset Settings"

    def __str__(self):
        return 'Asset Settings'

    def __unicode__(self):
        return self.__str__()

    def save(self, *args, **kwargs):
        """ Override to ensure only one instance exists
        """
        if AssetSettings.objects.exists() and not self.pk:
            raise ValidationError('There can only be one instance of the Site '
                                  'Administration Settings')
        else:
            return super(AssetSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """ Loads the Singleton Instance or returns None
        """
        try:
            obj = cls.objects.get(pk=1)
        except cls.DoesNotExist:
            obj = None
        return obj
