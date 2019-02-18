# -*- coding: utf-8 -*-
"""
Classes for blog syndication feeds.

:author: Douglas Daly
:date: 1/4/2019
"""
#
#   Imports
#
from abc import abstractmethod
from django.contrib.syndication.views import Feed

from .models import BlogSettings, Post, Category, Tag, Author


#
#   Base Class
#

class LatestFeed(Feed):
    """
    Base Syndication feed for latest posts
    """

    def __init__(self):
        super().__init__()
        blog_settings = BlogSettings.load()
        if blog_settings:
            self._max_posts = getattr(blog_settings, 'latest_feed_most_recent',
                                      5)
            self._title = getattr(blog_settings, 'title', "Blog")
            self._link = getattr(blog_settings, 'site_link', 'blog')
            self._show_authors = getattr(blog_settings, 'show_authors', False)
        else:
            self._max_posts = 5
            self._title = "Blog"
            self._link = "blog"
            self._show_authors = False

    def title(self, obj):
        return self._title

    def link(self, obj):
        return "/{}/".format(self._link.strip('/'))

    def description(self, obj):
        return "Latest posts from {}".format(self._title)

    def author_name(self, obj):
        return "Douglas Daly"

    def author_link(self, obj):
        return "https://www.douglasdaly.com/"

    def items(self, obj):
        return Post.get_displayable()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_author_name(self, item):
        if self._show_authors and item.author:
            return item.author.get_display_name()
        return None

    def item_author_email(self, item):
        if (self._show_authors and item.author and
                item.author.display_public_email):
            return item.author.public_contact_email
        return None

    def item_author_link(self, item):
        if self._show_authors and item.author:
            return item.author.get_absolute_url()
        return None

    def item_pubdate(self, item):
        return item.display_date


class ListingFeed(Feed):
    """
    Base Syndication feed for listing objects
    """
    author_name = "Douglas Daly"
    author_link = "https://www.douglasdaly.com/"

    def __init__(self, model):
        super().__init__()
        blog_settings = BlogSettings.load()
        if blog_settings:
            self._title = getattr(blog_settings, 'title', 'Blog')
            self._link = getattr(blog_settings, 'site_link', 'blog')
            self._show_authors = getattr(blog_settings, 'show_authors', False)
        else:
            self._title = "Blog"
            self._link = "blog"
            self._show_authors = False
        self._model = model

    def title(self):
        return "%s's %s" % (
            self._title, self._model._meta.verbose_name_plural.title()
        )

    @abstractmethod
    def link(self):
        pass

    @abstractmethod
    def description(self):
        pass

    def items(self):
        return self._model.objects.all()

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.get_absolute_url()


#
#   Implementation Classes
#

class CategoryListingFeed(ListingFeed):
    """
    Syndication feed for listing all blog categories
    """

    def __init__(self):
        super().__init__(Category)

    def link(self):
        return "/blog/categories.html"

    def description(self):
        return "Listing of all categories on the blog."


class TagListingFeed(ListingFeed):
    """
    Syndication feed for listing all blog tags
    """

    def __init__(self):
        super().__init__(Tag)

    def link(self):
        return "/blog/tags.html"

    def description(self):
        return "Listing of all tags on the blog."


class AuthorListingFeed(ListingFeed):
    """
    Syndication feed for listing all blog authors
    """

    def __init__(self):
        super().__init__(Author)

    def items(self):
        if self._show_authors:
            return self._model.get_displayable()
        return None

    def link(self):
        return "/blog/authors.html"

    def description(self):
        return "Listing of all authors on the blog."

    def item_title(self, item):
        return item.get_display_name()

    def item_description(self, item):
        return item.author_bio


class PostsLatestFeed(LatestFeed):
    """
    Syndication feed for most recent posts
    """

    def items(self, obj):
        return super().items(obj)[:self._max_posts]


class CategoryLatestFeed(LatestFeed):
    """
    Syndication feed for most recent posts for particular category
    """

    def get_object(self, request, slug):
        return Category.objects.get(slug=slug)

    def title(self, obj):
        return "{}, {} category".format(self._title, obj.name)

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return "Latest posts in the {} category.".format(obj.name)

    def items(self, obj):
        return super().items(obj).filter(category=obj)[:self._max_posts]


class TagLatestFeed(LatestFeed):
    """
    Syndication feed for most recent posts for particular tag
    """

    def get_object(self, request, slug):
        return Tag.objects.get(slug=slug)

    def title(self, obj):
        return "{}, {} tag".format(self._title, obj.name)

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return "Latest posts with the {} tag.".format(obj.name)

    def items(self, obj):
        return super().items(obj).filter(tags=obj)[:self._max_posts]


class AuthorLatestFeed(LatestFeed):
    """
    Syndication feed for most recent posts for particular author
    """

    def get_object(self, request, slug):
        return Author.get_displayable().get(slug=slug)

    def title(self, obj):
        return "{}, Posts from: {}".format(self._title, obj.get_display_name())

    def link(self, obj):
        if self._show_authors:
            return obj.get_absolute_url()
        return super().link(obj)

    def author_name(self, obj):
        if self._show_authors:
            return obj.get_display_name()
        return None

    def author_link(self, obj):
        if self._show_authors and obj.author_website:
            return obj.author_website
        return super().author_link(obj)

    def description(self, obj):
        if self._show_authors:
            return "Latest posts from {}.".format(obj.get_display_name())
        return "Latest posts"

    def items(self, obj):
        return obj.get_all_posts()[:self._max_posts]
