# -*- coding: utf-8 -*-
"""
Database Models for the blog app.

:author: Douglas Daly
:date: 12/4/2017
"""
#
#   Imports
#
import string
from datetime import datetime

from django.db import models
from django.urls import reverse, NoReverseMatch
from django.core.exceptions import ValidationError
from django.db.utils import OperationalError, ProgrammingError
from django.contrib.auth.models import User

from sorl.thumbnail import ImageField
from colorful.fields import RGBColorField

from .fields import ListField


#
#   Model definitions
#

class ColorTheme(models.Model):
    """
    Model for Color Themes with pre-set colors to use on the blog
    """
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, db_index=True)
    colors = ListField(null=False, blank=False)

    # - Meta class and dunder methods

    class Meta:
        verbose_name = "Color Theme"

    def __str__(self):
        return self.name

    def __unicode__(self):
        return str(self)


class BlogSettings(models.Model):
    """
    Singleton model for blog settings
    """
    title = models.CharField(max_length=100)
    site_link = models.CharField(max_length=40, null=False, default='blog')

    show_authors = models.BooleanField(default=False,
                                       verbose_name='Show Authors')

    posts_per_page = models.PositiveIntegerField(blank=False, default=10)
    latest_feed_most_recent = models.PositiveSmallIntegerField(
        null=False, default=5, verbose_name="Posts in Most Recent"
    )

    color_theme = models.ForeignKey(ColorTheme, on_delete=models.SET_NULL,
                                    null=True, default=None, blank=True)
    code_style_sheet = models.CharField(
        max_length=40, blank=False, default='code_default',
        choices=[('code_default', 'Default'), ('code_monokai', 'Dark')],
        verbose_name="Code Highlight Style"
    )

    # - Meta class and dunder methods

    class Meta:
        verbose_name_plural = "Blog Settings"

    def __str__(self):
        return 'Blog Settings'

    def __unicode__(self):
        return 'Blog Settings'

    # - Utility methods

    def save(self, *args, **kwargs):
        """Override to ensure only one instance exists"""
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
    """
    Model for post categories
    """
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    description = models.CharField(max_length=250, null=True, blank=True,
                                   default=None)

    icon_image = models.ImageField(upload_to="blog/categories/icons/",
                                   blank=True, null=True, default=None)
    color = RGBColorField(null=True, blank=True, default=None)
    font_class = models.CharField(max_length=80, default=None, blank=True,
                                  null=True, verbose_name="Font Class")

    search_terms = ListField(null=True, blank=True, default=None)

    # - Meta class and dunder methods

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def __unicode__(self):
        return '%s' % self.name

    # - Utility methods

    def get_absolute_url(self):
        return reverse('view_blog_category', kwargs={'slug': self.slug})


class Tag(models.Model):
    """
    Model for post tags
    """
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, db_index=True)
    description = models.CharField(max_length=200, null=True, default=None,
                                   blank=True)

    icon_image = models.ImageField(upload_to="blog/tags/icons/", null=True,
                                   blank=True, default=None)
    color = RGBColorField(null=True, default=None, blank=True)
    font_class = models.CharField(max_length=80, default=None, blank=True,
                                  null=True, verbose_name="Font Class")

    search_terms = ListField(null=True, blank=True, default=None,
                             verbose_name="Search Terms")

    _category = models.CharField(max_length=1, null=False)

    # - Meta classes and dunder methods

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return '%s' % self.name

    # - Methods

    def get_category_from_name(self):
        """Determine _category tag from objects name"""
        ret = self.name[0].upper()
        if ret not in string.ascii_uppercase:
            return "#"
        return ret

    # - Utility methods

    def save(self, *args, **kwargs):
        """Override to get _category trait on save"""
        self._category = self.get_category_from_name()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('view_blog_tag', kwargs={'slug': self.slug})


class CustomJS(models.Model):
    """
    Model for custom javascript files
    """
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=80, blank=True, null=True, default=None)
    slug = models.SlugField(max_length=180, db_index=True)
    file = models.FileField(upload_to="blog/posts/custom_js/")

    # - Meta class and dunder methods

    class Meta:
        ordering = ('tag', 'name')
        verbose_name = 'Custom JS'
        verbose_name_plural = "Custom JS Files"

    def __str__(self):
        return self.name

    def __unicode__(self):
        return '%s' % self.name


class CustomCSS(models.Model):
    """
    Model for custom CSS files
    """
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=80, blank=True, null=True, default=None)
    slug = models.SlugField(max_length=180, db_index=True)
    file = models.FileField(upload_to="blog/posts/custom_css/")

    # - Meta class and dunder methods

    class Meta:
        ordering = ('tag', 'name')
        verbose_name = 'Custom CSS'
        verbose_name_plural = "Custom CSS Files"

    def __str__(self):
        return self.name

    def __unicode__(self):
        return '%s' % self.name


class Author(models.Model):
    """
    Model for blog post authors
    """
    slug = models.SlugField(max_length=140, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, default=None,
                             blank=True, null=True)

    first_name = models.CharField(max_length=60, blank=False, null=False,
                                  verbose_name='First Name')
    last_name = models.CharField(max_length=60, blank=True, null=True,
                                 default=None, verbose_name='Last Name')
    display_name = models.CharField(
        max_length=80, blank=True, null=True, default=None,
        verbose_name="Pen Name (display)"
    )

    author_image = models.ImageField(upload_to="blog/authors/images/",
                                     null=True, default=None, blank=True,
                                     verbose_name="Author's Image")
    author_bio = models.TextField(null=True, default=None, blank=True,
                                  verbose_name="Author Biography")
    author_website = models.URLField(null=True, blank=True, default=None,
                                     verbose_name="Author's Website")

    contact_email = models.EmailField(null=True, blank=True, default=None,
                                      verbose_name="Contact Email")
    public_contact_email = models.EmailField(
        null=True, blank=True, default=None,
        verbose_name="Display Email (public)"
    )
    display_public_email = models.BooleanField(
        default=False, verbose_name="Display public email?"
    )

    is_active = models.BooleanField(default=True, verbose_name="Active")
    show_posts = models.BooleanField(default=True, verbose_name="Show Posts")

    # - Meta class and dunder methods

    class Meta:
        ordering = ('display_name', 'last_name', 'first_name')

    def __str__(self):
        return self.get_display_name()

    def __unicode__(self):
        return str(self)

    # - Methods

    def get_full_name(self):
        """Gets the authors full name"""
        ret = self.first_name
        if self.last_name:
            ret = "%s %s" % (ret, self.last_name)
        return ret

    def get_display_name(self):
        """Get the display name to use for the author"""
        if self.display_name:
            return self.display_name
        return self.get_full_name()

    def get_all_posts(self, displayed=True, previews=False):
        """Gets all posts associated with this author"""
        if displayed and self.is_active and self.show_posts:
            return Post.get_displayable(previews=previews)\
                .filter(author=self, published=True)
        return Post.objects.filter(author=self)

    # - Class methods

    @classmethod
    def get_displayable(cls):
        """Gets all authors which are displayable"""
        return cls.objects.filter(is_active=True)

    # - Utility methods

    def get_absolute_url(self):
        if self.is_active:
            return reverse('view_blog_author', kwargs={'slug': self.slug})
        raise NoReverseMatch()

    def save(self, *args, **kwargs):
        """Override save to change author's posts on certain events"""
        if self.pk is not None:
            curr = Author.get(pk=self.pk)
            if not self.is_active or (not self.show_posts and
                                      curr.show_posts != self.show_posts):
                auth_posts = self.get_all_posts(displayed=False)
                for post in auth_posts:
                    post.published = False
                    post.save()
        super().save(*args, **kwargs)


class Post(models.Model):
    """
    Model for blog posts
    """
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True,
                            verbose_name='Link Slug')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True,
                               blank=True, default=None)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    icon_image = ImageField(upload_to="blog/posts/icons/", default=None,
                            blank=True, null=True, verbose_name="Icon Image")

    description = models.TextField(default="", null=True)
    body = models.TextField()

    search_terms = ListField(null=True, blank=True, default=None,
                             verbose_name="Search Terms")

    custom_javascript = models.FileField(
        upload_to="blog/posts/scripts/", blank=True, default=None, null=True,
        verbose_name="Custom Javascript"
    )
    css_includes = models.ManyToManyField(
        CustomCSS, blank=True, verbose_name="CSS Includes"
    )
    javascript_includes = models.ManyToManyField(
        CustomJS, blank=True, verbose_name="Javascript Includes"
    )

    created = models.DateTimeField(db_index=True, auto_now_add=True,
                                   editable=False)
    last_updated = models.DateTimeField(verbose_name='Last Updated',
                                        auto_now=True, editable=False)
    posted = models.DateTimeField(db_index=True, null=True, blank=True,
                                  default=datetime.now(), editable=False)
    publish_date = models.DateTimeField(db_index=True, null=True, blank=True,
                                        editable=True, default=datetime.now())
    display_date = models.DateTimeField(db_index=True, editable=False,
                                        verbose_name="Display Date")

    previewable = models.BooleanField(default=False, verbose_name='Preview')
    published = models.BooleanField(default=False, verbose_name='Publish')

    # - Meta class and dunder methods

    class Meta:
        ordering = ('-display_date',)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return '%s' % self.title

    # - Class methods

    @classmethod
    def get_displayable(cls, previews=False):
        """Gets displayable posts"""
        qry = models.Q(published=True)
        if previews:
            qry |= models.Q(previewable=True)
        return cls.objects.filter(qry).exclude(author__is_active=False)

    # - Helper methods

    def _get_display_date(self):
        """datetime: Display date to use"""
        if self.published:
            return self.publish_date
        return self.last_updated

    # - Utility methods

    def get_absolute_url(self):
        return reverse('view_blog_post', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """Custom save method for handling dates"""
        self.last_updated = datetime.now()

        if self.published:
            self.previewable = False

        self.display_date = self._get_display_date()

        if self.pk is not None:
            curr = Post.objects.get(pk=self.pk)
            if not curr.published and self.published:
                self.posted = datetime.now()
        else:
            if self.published:
                self.posted = datetime.now()

        super().save(*args, **kwargs)
