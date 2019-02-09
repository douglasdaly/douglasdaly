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
import string
from datetime import datetime

from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db.utils import OperationalError, ProgrammingError
from django.contrib.auth.models import User

from sorl.thumbnail import ImageField

from .fields import ListField


#
#   Model definitions
#

class BlogSettings(models.Model):
    """Singleton model for blog settings"""
    title = models.CharField(max_length=100, db_index=True)
    site_link = models.CharField(max_length=40, null=False, default='blog')

    posts_per_page = models.PositiveIntegerField(blank=False, default=10)
    code_style_sheet = models.CharField(max_length=40, blank=False,
                                        default='code_default',
                                        choices=[
                                            ('code_default', 'Default'),
                                            ('code_monokai', 'Monokai')
                                        ])

    latest_feed_most_recent = models.PositiveSmallIntegerField(null=False,
                                                               default=5)

    class Meta:
        verbose_name_plural = "Blog Settings"

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
        except OperationalError:
            obj = None
        except ProgrammingError:
            obj = None
        return obj


class Category(models.Model):
    """Model for post categories"""
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    description = models.CharField(max_length=250, null=True, blank=True,
                                   default=None)

    icon_image = models.ImageField(upload_to="blog/categories/icons/",
                                   blank=True, null=True, default=None)

    search_terms = ListField(null=True, blank=True, default=None)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def __unicode__(self):
        return '%s' % self.name

    def get_absolute_url(self):
        return reverse('view_blog_category', kwargs={'slug': self.slug})


class Tag(models.Model):
    """Model for post tags"""
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, db_index=True)
    description = models.CharField(max_length=200, null=True, default=None,
                                   blank=True)

    image = models.ImageField(upload_to="blog/tags/icons/", null=True,
                              blank=True, default=None)

    search_terms = ListField(null=True, blank=True, default=None)

    _category = models.CharField(max_length=1, null=False)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        self._category = self.__get_category_from_name()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('view_blog_tag', kwargs={'slug': self.slug})

    def __get_category_from_name(self):
        ret = self.name[0].upper()
        if ret not in string.ascii_uppercase:
            return "#"
        return ret


class CustomJS(models.Model):
    """Model for custom javascript files"""
    name = models.CharField(max_length=100, unique=True)
    file = models.FileField(upload_to="blog/posts/custom_js/")
    tag = models.CharField(max_length=80, blank=True, null=True, default=None)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('tag', 'name',)
        verbose_name_plural = "Custom JS Files"


class CustomCSS(models.Model):
    """Model for custom CSS files"""
    name = models.CharField(max_length=100, unique=True)
    file = models.FileField(upload_to="blog/posts/custom_css/")
    tag = models.CharField(max_length=80, blank=True, null=True, default=None)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('tag', 'name',)
        verbose_name_plural = "Custom CSS Files"


class Author(models.Model):
    """Model for blog post authors"""
    pen_name_full = models.CharField(max_length=120, blank=False, null=False)
    pen_name_short = models.CharField(max_length=80, blank=True, null=True,
                                      default=None)
    author_image = models.ImageField(upload_to="blog/authors/images/",
                                     null=True, default=None, blank=True)

    contact_email = models.EmailField(null=True, blank=True, default=None)
    public_contact_email = models.EmailField(null=True, blank=True,
                                             default=True)
    display_public_email = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, default=None,
                             blank=True, null=True)

    # - Methods

    def get_all_posts(self):
        """Gets all posts associated with this author"""
        return Post.objects.get(author=self).all()


class Post(models.Model):
    """Model for blog posts"""
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True,
                               blank=True, default=None)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    icon_image = ImageField(upload_to="blog/posts/icons/", default=None,
                            blank=True, null=True)

    description = models.TextField(default="", null=True)
    body = models.TextField()

    search_terms = ListField(null=True, blank=True, default=None)

    custom_javascript = models.FileField(upload_to="blog/posts/scripts/",
                                         blank=True, default=None, null=True)
    css_includes = models.ManyToManyField(CustomCSS, blank=True)
    javascript_includes = models.ManyToManyField(CustomJS, blank=True)

    created = models.DateTimeField(db_index=True, auto_now_add=True)
    posted = models.DateTimeField(db_index=True, null=True, blank=True,
                                  default=None)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ('-posted',)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return '%s' % self.title

    def get_absolute_url(self):
        return reverse('view_blog_post', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.pk is not None:
            curr = Post.objects.get(pk=self.pk)
            if not curr.published and self.published:
                self.posted = datetime.now()
        else:
            if self.published:
                self.posted = datetime.now()

        super().save(*args, **kwargs)
