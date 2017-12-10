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
from django.db.models import permalink


#
#   Model Definitions
#

class Page(models.Model):
    title = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    content = models.TextField()
    link_name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return "%s" % self.title

    @permalink
    def get_absolute_url(self):
        return 'view_page', None, {'slug': self.slug}
