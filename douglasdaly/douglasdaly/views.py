# -*- coding: utf-8 -*-
"""
douglasdaly/views.py

    Views for the main site pages

@author: Douglas Daly
@date: 12/10/2017
"""
#
#   Imports
#
import os

from django.shortcuts import render, get_object_or_404
from django.http import Http404

from sentry_sdk import last_event_id, capture_message

from .models import Page, SiteSettings, SiteAdminSettings
from blog.models import Post


#
#   View Functions
#

def index(request):
    """Home page view"""
    site_settings = SiteSettings.load()
    recent_posts = Post.objects.all() \
                   .filter(published=True)[:site_settings.number_recent_posts]

    if site_settings.number_recent_posts > 0 and len(recent_posts) > 0:
        post_col_width = int(12 / len(recent_posts))
    else:
        post_col_width = 0

    return render(request, "index.html", {
        'settings': site_settings,
        'recent_posts': recent_posts,
        'post_col_width': post_col_width,
        'home_show_card': site_settings.home_show_card,
        'home_tagline': site_settings.home_tagline,
        'home_image': site_settings.home_image,
    })


def view_page(request, slug):
    """Generic page view"""
    page = get_object_or_404(Page, slug=slug)
    if not page.published:
        raise Http404

    site_settings = SiteSettings.load()
    return render(request, "view_page.html", {
        'settings': site_settings,
        'page': page,
        'custom_css_file': page.custom_css,
    })


def inactive_view(request):
    """Site inactive view"""
    admin_settings = SiteAdminSettings.load()
    if admin_settings.site_is_active:
        raise Http404

    return render(request, "generic.html", {
        "generic_title": admin_settings.inactive_page_title,
        "generic_content": admin_settings.inactive_page_content
    })


def custom_404_view(request, exception):
    admin_settings = SiteAdminSettings.load()

    ret_data = {
        "generic_title": admin_settings.err_404_title,
        "generic_content": admin_settings.err_404_content
    }
    if admin_settings.err_404_sentry:
        capture_message("Page not found", level="warning")

    return render(request, "generic.html", ret_data, status=404)


def custom_500_view(request):
    admin_settings = SiteAdminSettings.load()

    ret_data = {
        "generic_title": admin_settings.err_500_title,
        "generic_content": admin_settings.err_500_content
    }
    if admin_settings.err_500_sentry:
        ret_data['sentry_event_id'] = last_event_id()
        ret_data['sentry_dsn'] = os.environ.get('SENTRY_DSN')

    return render(request, "errors/500.html", ret_data, status=500)
