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

    return render_to_response('blog/index.html', {
        'blog_settings': blog_settings,
        'posts': __get_post_page(post_list, page=page,
                                 blog_settings=blog_settings),
    })


def view_post(request, slug):
    return render_to_response('blog/view_post.html', {
        'post': get_object_or_404(Post, slug=slug),
    })


def view_categories(request):
    categories = Category.objects.all()
    return render_to_response('blog/categories.html', {
        'categories': categories,
    })


def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)

    blog_settings = BlogSettings.load()
    page = request.GET.get("page")

    return render_to_response('blog/view_category.html', {
        'category': category,
        'posts': __get_post_page(Post.objects.filter(category=category), page,
                                 blog_settings),
    })


def view_tags(request):
    tags = Tag.objects.all()
    return render_to_response('blog/tags.html', {
        'tags': tags,
    })


def view_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)

    blog_settings = BlogSettings.load()
    page = request.GET.get("page")

    return render_to_response('blog/view_tag.html', {
        'tag': tag,
        'posts': __get_post_page(Post.objects.filter(tags=tag), page,
                                 blog_settings),
    })


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
