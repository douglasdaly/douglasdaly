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

from adminsortable.models import SortableMixin


#
#   Model Definitions
#

class Page(SortableMixin):
    title = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    link_name = models.CharField(max_length=40, unique=True)
    passthrough_page = models.BooleanField(default=False)
    passthrough_link = models.CharField(max_length=40, default=None, null=True)
    custom_css = models.CharField(max_length=80, default=None, null=True)
    content = models.TextField(default=None, null=True)

    class Meta:
        ordering = ['the_order']

    the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return "%s" % self.title

    def get_absolute_url(self):
        if not self.passthrough_page:
            return reverse('view_page', kwargs={'slug': self.slug})
        else:
            return self.passthrough_link
