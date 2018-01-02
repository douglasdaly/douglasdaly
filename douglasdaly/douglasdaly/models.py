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

from adminsortable.models import SortableMixin


#
#   Model Definitions
#

class SiteSettings(models.Model):
    title = models.CharField(max_length=20, unique=True)
    meta_description = models.CharField(max_length=120, null=True)
    meta_author = models.CharField(max_length=100, null=True)
    google_analytics_key = models.CharField(max_length=120, null=True,
                                            blank=True)
    github_link = models.URLField(null=True, blank=True)
    linkedin_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return 'Site Settings'

    def __unicode__(self):
        return "Site Settings"

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


class Page(SortableMixin):
    title = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    link_name = models.CharField(max_length=40, unique=True)
    passthrough_page = models.BooleanField(default=False)
    passthrough_link = models.CharField(max_length=40, default=None, null=True,
                                        blank=True)
    custom_css = models.CharField(max_length=80, default=None, null=True,
                                  blank=True)
    content = models.TextField(default=None, null=True)

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
