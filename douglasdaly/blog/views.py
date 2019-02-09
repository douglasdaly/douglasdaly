# -*- coding: utf-8 -*-
"""
blog/views.py

    Views setup for the blog application

"""
#
#   Imports
#
import re

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed, Http404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Post, Category, Tag, BlogSettings


#
#   Views
#

def index(request):
    blog_settings = BlogSettings.load()

    post_list = Post.objects.all()
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
    blog_settings = BlogSettings.load()
    page = request.GET.get("page")

    query_string = ''
    found_entries = None

    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = __get_query(query_string, ['title', 'description',
                                                 'category__name',
                                                 'tags__name', ])
        found_entries = Post.objects.filter(entry_query).distinct()

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
    post = get_object_or_404(Post, slug=slug)

    if not post.published:
        raise Http404

    ret_dict = {
        'post': post,
    }
    ret_dict = __append_common_vars(request, ret_dict)

    return render(request, 'blog/view_post.html', ret_dict)


def view_categories(request):
    categories = Category.objects.all()

    ret_dict = {
        'categories': categories,
        'view_rss': 'rss/categories.xml',
        'current_nav': 'categories',
    }
    ret_dict = __append_common_vars(request, ret_dict)

    return render(request, 'blog/categories.html', ret_dict)


def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)

    blog_settings = BlogSettings.load()
    page = request.GET.get("page")

    ret_dict = {
        'category': category,
        'posts': __get_post_page(Post.objects.filter(category=category), page,
                                 blog_settings),
        'blog_settings': blog_settings,
        'view_rss': 'rss/categories/{}.xml'.format(category.slug),
    }
    ret_dict = __append_common_vars(request, ret_dict, include_settings=False)

    return render(request, 'blog/view_category.html', ret_dict)


def view_tags(request):
    tags = Tag.objects.all()

    ret_dict = {
        'tags': tags,
        'view_rss': 'rss/tags.xml',
        'current_nav': 'tags',
    }
    ret_dict = __append_common_vars(request, ret_dict)

    return render(request, 'blog/tags.html', ret_dict)


def view_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)

    blog_settings = BlogSettings.load()
    page = request.GET.get("page")

    ret_dict = {
        'tag': tag,
        'posts': __get_post_page(Post.objects.filter(tags=tag), page,
                                 blog_settings),
        'blog_settings': blog_settings,
        'view_rss': 'rss/tag/{}.xml'.format(tag.slug),
    }
    ret_dict = __append_common_vars(request, ret_dict, include_settings=False)

    return render(request, 'blog/view_tag.html', ret_dict)


#
#   Session Helper Views
#

def update_side_menu_sort(request, sort_tab):
    """ Helper Function to update the Sort on the side menu for persistence
    """
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST', ])

    request.session['sort_tab'] = sort_tab
    return HttpResponse('OK')


#
#   Helper Functions
#

def __get_post_page(post_list, page=1, blog_settings=None):
    post_list = post_list.filter(published=True)
    if blog_settings is None:
        per_page = 10
    else:
        per_page = blog_settings.posts_per_page

    if page is None:
        page = 1

    post_paginator = Paginator(post_list, per_page)

    return post_paginator.get_page(page)


def __append_common_vars(request, curr_dict, include_settings=True):
    sort_tab = request.session.get('sort_tab', 'date')

    rss_categories = Category.objects.all()
    rss_tags = Tag.objects.all()

    common_dict = {
        'sort_tab': sort_tab,
        'rss_categories': rss_categories,
        'rss_tags': rss_tags,
    }

    if include_settings:
        blog_settings = BlogSettings.load()
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
