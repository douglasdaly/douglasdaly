# -*- coding: utf-8 -*-
"""
Views for the blog application

:author: Douglas Daly
:date: 2/16/2019
"""
#
#   Imports
#
import re

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed, Http404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Post, Category, Tag, BlogSettings, Author


#
#   Views
#

def index(request):
    """Blog home page view"""
    blog_settings = BlogSettings.load()

    post_list = Post.get_displayable().all()
    page = request.GET.get("page")

    ret_dict = {
        'blog_settings': blog_settings,
        'posts': __get_post_page(post_list, page=page,
                                 blog_settings=blog_settings),
        'view_rss': 'rss/latest.xml',
        'current_nav': 'home',
    }
    ret_dict = __append_common_vars(request, ret_dict, include_settings=False)

    return render(request, 'blog/index.html', ret_dict)


def search(request):
    """Search page view"""
    blog_settings = BlogSettings.load()
    page = request.GET.get("page")

    query_string = ''
    found_entries = None

    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = __get_query(query_string, ['title', 'description',
                                                 'category__name',
                                                 'tags__name', ])
        found_entries = Post.get_displayable().filter(entry_query).distinct()

    if found_entries is not None:
        posts = __get_post_page(found_entries, page=page,
                                blog_settings=blog_settings)
    else:
        posts = None

    ret_dict = {
        'query_string': query_string,
        'posts': posts,
        'blog_settings': blog_settings,
        'current_nav': 'search',
    }
    ret_dict = __append_common_vars(request, ret_dict, include_settings=False)

    return render(request, 'blog/search.html', ret_dict)


def view_post(request, slug):
    """View post view"""
    post = get_object_or_404(Post, slug=slug)

    if not post.published:
        raise Http404

    ret_dict = {
        'post': post,
    }
    ret_dict = __append_common_vars(request, ret_dict)

    return render(request, 'blog/view_post.html', ret_dict)


def view_categories(request):
    """View category posts view"""
    categories = Category.objects.all()

    ret_dict = {
        'categories': categories,
        'view_rss': 'rss/categories.xml',
        'current_nav': 'categories',
    }
    ret_dict = __append_common_vars(request, ret_dict)

    return render(request, 'blog/categories.html', ret_dict)


def view_category(request, slug):
    """View all categories view"""
    category = get_object_or_404(Category, slug=slug)

    blog_settings = BlogSettings.load()
    page = request.GET.get("page")

    ret_dict = {
        'category': category,
        'posts': __get_post_page(Post.get_displayable()
                                     .filter(category=category),
                                 page=page, blog_settings=blog_settings),
        'blog_settings': blog_settings,
        'view_rss': 'rss/categories/{}.xml'.format(category.slug),
    }
    ret_dict = __append_common_vars(request, ret_dict, include_settings=False)

    return render(request, 'blog/view_category.html', ret_dict)


def view_authors(request):
    """View all authors view"""
    blog_settings = BlogSettings.load()
    if not blog_settings.show_authors:
        raise Http404

    authors = Author.get_displayable()

    ret_dict = {
        'authors': authors,
        'view_rss': 'rss/authors.xml',
        'current_nav': 'authors',
    }
    ret_dict = __append_common_vars(request, ret_dict)

    return render(request, 'blog/authors.html', ret_dict)


def view_author(request, slug):
    """View individual author's posts"""
    blog_settings = BlogSettings.load()
    if not blog_settings.show_authors:
        raise Http404

    author = get_object_or_404(Author, slug=slug)
    if not author.is_active:
        raise Http404

    page = request.GET.get("page")

    ret_dict = {
        'author': author,
        'posts': __get_post_page(Post.get_displayable().filter(author=author),
                                 page=page, blog_settings=blog_settings),
        'blog_settings': blog_settings,
        'view_rss': 'rss/author/{}.xml'.format(author.slug),
    }
    ret_dict = __append_common_vars(request, ret_dict, include_settings=False)

    return render(request, 'blog/view_author.html', ret_dict)


def view_tags(request):
    """View all tags view"""
    tags = Tag.objects.all()

    ret_dict = {
        'tags': tags,
        'view_rss': 'rss/tags.xml',
        'current_nav': 'tags',
    }
    ret_dict = __append_common_vars(request, ret_dict)

    return render(request, 'blog/tags.html', ret_dict)


def view_tag(request, slug):
    """View all posts for the specified tag"""
    tag = get_object_or_404(Tag, slug=slug)

    blog_settings = BlogSettings.load()
    page = request.GET.get("page")

    ret_dict = {
        'tag': tag,
        'posts': __get_post_page(Post.get_displayable().filter(tags=tag),
                                 page=page, blog_settings=blog_settings),
        'blog_settings': blog_settings,
        'view_rss': 'rss/tag/{}.xml'.format(tag.slug),
    }
    ret_dict = __append_common_vars(request, ret_dict, include_settings=False)

    return render(request, 'blog/view_tag.html', ret_dict)


#
#   Session Helper Views
#

def update_side_menu_sort(request, sort_tab):
    """Helper Function to update the Sort on the side menu for persistence"""
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST', ])

    request.session['sort_tab'] = sort_tab
    return HttpResponse('OK')


#
#   Helper Functions
#

def __get_post_page(post_list, page=1, blog_settings=None):
    """Helper function to get posts for specified page based on settings"""
    if blog_settings is None:
        per_page = 10
    else:
        per_page = blog_settings.posts_per_page

    if page is None:
        page = 1

    post_paginator = Paginator(post_list, per_page)

    return post_paginator.get_page(page)


def __append_common_vars(request, curr_dict, include_settings=True):
    """Appends common variables needed by app pages to return dictionary"""
    sort_tab = request.session.get('sort_tab', 'date')

    blog_settings = BlogSettings.load()

    rss_categories = Category.objects.all()
    rss_tags = Tag.objects.all()

    if blog_settings.show_authors:
        rss_authors = Author.get_displayable()
    else:
        rss_authors = None

    common_dict = {
        'sort_tab': sort_tab,
        'rss_categories': rss_categories,
        'rss_tags': rss_tags,
        'rss_authors': rss_authors,
    }

    if include_settings:
        common_dict["blog_settings"] = blog_settings

    return {**curr_dict, **common_dict}


def __normalize_query(query_string,
                      findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                      normspace=re.compile(r'\s{2,}').sub):
    """Normalized query string into individual words for searching"""
    return [normspace(' ', (t[0] or t[1]).strip()) for t
            in findterms(query_string)]


def __get_query(query_string, search_fields):
    """Gets a Query for searching models with"""
    query = None

    terms = __normalize_query(query_string)
    for term in terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query

    return query
