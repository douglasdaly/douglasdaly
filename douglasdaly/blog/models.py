# -*- coding: utf-8 -*-
"""
blog/models.py

    Database Models for the blog app.

@author: Douglas Daly
@date: 12/4/2017
"""
#
#   Imports
#
from django.db import models
from django.db.models import permalink


#
#   Model Definitions
#

class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()
    posted = models.DateTimeField(db_index=True, auto_now_add=True)
    category = models.ForeignKey('blog.Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return 'view_blog_post', None, { 'slug': self.slug }


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return 'view_blog_category', None, { 'slug': self.slug }
