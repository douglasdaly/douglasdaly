# -*- coding: utf-8 -*-
"""
views.py

    Views for the main site pages

@author: Douglas Daly
@date: 12/10/2017
"""
#
#   Imports
#
from django.shortcuts import render_to_response, get_object_or_404
from django.http import JsonResponse, Http404

from sorl.thumbnail import get_thumbnail

from .models import Page, SiteSettings, FileAsset, ImageAsset
from blog.models import Post


#
#   View Functions
#

def index(request):
    settings = SiteSettings.load()
    recent_posts = Post.objects.all() \
                       .filter(published=True)[:settings.number_recent_posts]

    if settings.number_recent_posts > 0 and len(recent_posts) > 0:
        post_col_width = int(12 / len(recent_posts))
    else:
        post_col_width = 0

    return render_to_response("index.html", {
        'settings': settings,
        'recent_posts': recent_posts,
        'post_col_width': post_col_width,
    })


def view_page(request, slug):
    settings = SiteSettings.load()
    page = get_object_or_404(Page, slug=slug)
    return render_to_response("view_page.html", {
        'settings': settings,
        'page': page,
        'custom_css_file': page.custom_css,
    })


def get_asset(request):
    slug = request.GET.get("slug", None)
    asset_type = request.GET.get("type", None)

    if asset_type == "file":
        asset = get_object_or_404(FileAsset, slug=slug)

        data = {
            'title': asset.title,
            'description': asset.description,
            'url': asset.asset.url
        }

    elif asset_type == "image":
        asset = get_object_or_404(ImageAsset, slug=slug)

        size = request.GET.get("size", None)
        crop = request.GET.get("crop", None)
        quality = request.GET.get("quality", None)

        if size is not None:
            new_im = get_thumbnail(asset.asset, size, crop=crop, quality=quality)
        else:
            new_im = asset.asset

        data = {
            'title': asset.title,
            'description': asset.description,
            'url': new_im.url
        }

    else:
        return Http404("Invalid asset type")

    return JsonResponse(data)
