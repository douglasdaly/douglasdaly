# -*- coding: utf-8 -*-
"""
douglasdaly/blog/feeds.py

    Classes for blog syndication feeds.

@author: Douglas Daly
@date: 1/4/2019
"""
#
#   Imports
#
from abc import abstractmethod
from django.contrib.syndication.views import Feed

from .models import BlogSettings, Post, Category, Tag


#
#   Base Class
#

class LatestFeed(Feed):
    """Base Syndication feed for latest posts"""

    author_name = "Douglas Daly"
    author_link = "https://www.douglasdaly.com/"
    item_author_name = "Douglas Daly"

    def __init__(self):
        super().__init__()
        blog_settings = BlogSettings.load()
        if blog_settings:
            self._max_posts = blog_settings.latest_feed_most_recent
            self._title = blog_settings.title
            self._link = blog_settings.site_link
        else:
            self._max_posts = 5
            self._title = "Blog"
            self._link = "blog"

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def title(self, obj):
        return self._title

    def link(self, obj):
        return "/{}/".format(self._link.strip('/'))

    def description(self, obj):
        return "Latest posts from {}".format(self._title)


class ListingFeed(Feed):
    """Base Syndication feed for listing objects"""

    author_name = "Douglas Daly"
    author_link = "https://www.douglasdaly.com/"

    def __init__(self, model):
        super().__init__()
        blog_settings = BlogSettings.load()
        if blog_settings:
            self._title = blog_settings.title
            self._link = blog_settings.site_link
        else:
            self._title = "Blog"
            self._link = "blog"
        self._model = model

    def items(self):
        return self._model.objects.all().order_by('name')

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def title(self):
        return "{}'s {}".format(self._title,
                                self._model._meta.verbose_name_plural.title())

    @abstractmethod
    def link(self):
        pass

    @abstractmethod
    def description(self):
        pass


#
#   Implementation Classes
#

class CategoryListingFeed(ListingFeed):
    """Syndication feed for listing all blog categories"""

    def __init__(self):
        super().__init__(Category)

    def link(self):
        return "/blog/categories.html"

    def description(self):
        return "Listing of all categories on the blog."


class TagListingFeed(ListingFeed):
    """Syndication feed for listing all blog tags"""

    def __init__(self):
        super().__init__(Tag)

    def link(self):
        return "/blog/tags.html"

    def description(self):
        return "Listing of all tags on the blog."


class PostsLatestFeed(LatestFeed):
    """Syndication feed for most recent posts"""

    def items(self):
        return Post.objects.filter(published=True) \
                   .order_by('-posted')[:self._max_posts]


class CategoryLatestFeed(LatestFeed):
    """Syndication feed for most recent posts for particular category"""

    def get_object(self, request, slug):
        return Category.objects.get(slug=slug)

    def title(self, obj):
        return "{}, {} category".format(self._title, obj.name)

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return "Latest posts in the {} category.".format(obj.name)

    def items(self, obj):
        return Post.objects.filter(category=obj, published=True) \
                   .order_by('-posted')[:self._max_posts]


class TagLatestFeed(LatestFeed):
    """Syndication feed for most recent posts for particular tag"""

    def get_object(self, request, slug):
        return Tag.objects.get(slug=slug)

    def title(self, obj):
        return "{}, {} tag".format(self._title, obj.name)

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return "Latest posts with the {} tag.".format(obj.name)

    def items(self, obj):
        return Post.objects.filter(tags=obj, published=True) \
                   .order_by('-posted')[:self._max_posts]
