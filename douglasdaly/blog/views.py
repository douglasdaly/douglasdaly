#
#   Imports
#
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator

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
    }
    ret_dict = __append_common_vars(request, ret_dict)

    return render_to_response('blog/index.html', ret_dict)


def view_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    ret_dict = {
        'post': post,
    }
    ret_dict = __append_common_vars(request, ret_dict)

    return render_to_response('blog/view_post.html', ret_dict)


def view_categories(request):
    categories = Category.objects.all()

    ret_dict = {
        'categories': categories,
    }
    ret_dict = __append_common_vars(request, ret_dict)

    return render_to_response('blog/categories.html', ret_dict)


def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)

    blog_settings = BlogSettings.load()
    page = request.GET.get("page")

    ret_dict = {
        'category': category,
        'posts': __get_post_page(Post.objects.filter(category=category), page,
                                 blog_settings),
    }
    ret_dict = __append_common_vars(request, ret_dict)

    return render_to_response('blog/view_category.html', ret_dict)


def view_tags(request):
    tags = Tag.objects.all()

    ret_dict = {
        'tags': tags,
    }
    ret_dict = __append_common_vars(request, ret_dict)

    return render_to_response('blog/tags.html', ret_dict)


def view_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)

    blog_settings = BlogSettings.load()
    page = request.GET.get("page")

    ret_dict = {
        'tag': tag,
        'posts': __get_post_page(Post.objects.filter(tags=tag), page,
                                 blog_settings),
    }
    ret_dict = __append_common_vars(request, ret_dict)

    return render_to_response('blog/view_tag.html', ret_dict)


#
#   Helper Functions
#

def __get_post_page(post_list, page=1, blog_settings=None):
    if blog_settings is None:
        per_page = 10
    else:
        per_page = blog_settings.posts_per_page

    if page is None:
        page = 1

    post_paginator = Paginator(post_list, per_page)

    return post_paginator.get_page(page)


def __append_common_vars(request, curr_dict):
    sort_tab = request.session.get('sort_tab', 'date')

    common_dict = {'sort_tab': sort_tab}

    return {**curr_dict, **common_dict}
