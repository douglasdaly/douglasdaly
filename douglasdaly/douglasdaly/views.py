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

from .models import Page


#
#   View Functions
#

def index(request):
    return render_to_response("index.html")


def view_page(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render_to_response("view_page.html", {
        'page': page,
        'custom_css_file': page.custom_css
    })
