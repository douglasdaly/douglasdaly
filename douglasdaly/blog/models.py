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
from django.urls import reverse
from django.core.exceptions import ValidationError


#
#   Model Definitions
#

class BlogSettings(models.Model):
    title = models.CharField(max_length=100, db_index=True)

    posts_per_page = models.PositiveIntegerField(blank=False, default=10)

    def __str__(self):
        return 'Blog Settings'

    def __unicode__(self):
        return 'Blog Settings'

    def save(self, *args, **kwargs):
        """ Override to ensure only one instance exists
        """
        if BlogSettings.objects.exists() and not self.pk:
            raise ValidationError('There can only be one instance of the Site '
                                  'Settings')
        else:
            return super(BlogSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """ Loads the Singleton Instance or returns None
        """
        try:
            obj = cls.objects.get(pk=1)
        except cls.DoesNotExist:
            obj = None
        return obj


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return '%s' % self.name

    def get_absolute_url(self):
        return reverse('view_blog_category', kwargs={'slug': self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, db_index=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return '%s' % self.name

    def get_absolute_url(self):
        return reverse('view_blog_tag', kwargs={'slug': self.slug})


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    icon_image = models.CharField(max_length=120, null=True, default=None,
                                  blank=True)
    description = models.TextField(default="", null=True)

    body = models.TextField()
    posted = models.DateTimeField(db_index=True, auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ('-posted',)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return '%s' % self.title

    def get_absolute_url(self):
        return reverse('view_blog_post', kwargs={'slug': self.slug})
