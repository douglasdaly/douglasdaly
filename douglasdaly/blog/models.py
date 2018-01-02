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


#
#   Model Definitions
#

class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(default="", null=True)
    body = models.TextField()
    posted = models.DateTimeField(db_index=True, auto_now_add=True)
    category = models.ForeignKey('blog.Category', on_delete=models.CASCADE)

    tags = models.ManyToManyField('blog.Tag', through='PostToTag', blank=True)

    class Meta:
        ordering = ['-posted']

    def __str__(self):
        return self.title

    def __unicode__(self):
        return '%s' % self.title

    def get_absolute_url(self):
        return reverse('view_blog_post', kwargs={'slug': self.slug})


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def __unicode__(self):
        return '%s' % self.title

    def get_absolute_url(self):
        return reverse('view_blog_category', kwargs={'slug': self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, db_index=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return '%s' % self.name

    def get_absolute_url(self):
        return reverse('view_blog_tag', kwargs={'slug': self.slug})


class PostToTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, db_index=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return self.post.slug + " -> " + self.tag.slug

    def __unicode__(self):
        return '%s -> %s' % (self.post.slug, self.tag.slug)
