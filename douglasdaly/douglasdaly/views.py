# -*- coding: utf-8 -*-
"""
view.py

    Views for the main site pages

@author: Douglas Daly
@date: 12/10/2017
"""
#
#   Imports
#
from django.shortcuts import render_to_response, get_object_or_404

from .models import Page, SiteSettings
from blog.models import Post


#
#   View Functions
#

def index(request):
    settings = SiteSettings.load()
    recent_posts = Post.objects.all()[:settings.number_recent_posts]

    if settings.number_recent_posts > 0:
        post_col_width = int(12 / settings.number_recent_posts)
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
