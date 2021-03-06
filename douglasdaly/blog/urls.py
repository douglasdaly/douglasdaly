
#
#   Imports
#
from django.conf.urls import url
from django.urls import path

from . import views
from .feeds import (PostsLatestFeed, CategoryLatestFeed, TagLatestFeed,
                    CategoryListingFeed, TagListingFeed, AuthorListingFeed,
                    AuthorLatestFeed)


#
#   Patterns
#

urlpatterns = [
    # - Views
    url(
        r'^$',
        views.index,
        name='blog_home'
    ),
    url(
        r'^view/(?P<slug>[^\.]+).html',
        views.view_post,
        name='view_blog_post'
    ),
    url(
        r'^categories.html',
        views.view_categories,
        name="view_blog_categories"
    ),
    url(
        r'^categories/(?P<slug>[^\.]+).html',
        views.view_category,
        name='view_blog_category'
    ),
    url(
        r'^authors.html',
        views.view_authors,
        name="view_blog_authors"
    ),
    url(
        r'^authors/(?P<slug>[^\.]+).html',
        views.view_author,
        name='view_blog_author'
    ),
    url(
        r'^tags.html',
        views.view_tags,
        name="view_blog_tags"
    ),
    url(
        r'^tags/(?P<slug>[^\.]+).html',
        views.view_tag,
        name='view_blog_tag'
    ),
    url(
        r'^update_sort_tab/(?P<sort_tab>[^\.]+)',
        views.update_side_menu_sort,
        name="update_side_menu_sort"
    ),
    url(
        r'^search.html',
        views.search,
        name="search"
    ),

    # - Feeds
    path('rss/latest.xml', PostsLatestFeed()),
    path('rss/categories.xml', CategoryListingFeed()),
    path('rss/authors.xml', AuthorListingFeed()),
    path('rss/tags.xml', TagListingFeed()),
    path('rss/category/<str:slug>.xml', CategoryLatestFeed()),
    path('rss/tag/<str:slug>.xml', TagLatestFeed()),
    path('rss/author/<str:slug>.xml', AuthorLatestFeed()),
]
