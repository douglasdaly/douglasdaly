# -*- coding: utf-8 -*-
"""
page_tags.py

    Access to page links for base template.

@author: Douglas Daly
@date: 12/10/2017
"""
#
#   Imports
#
from django import template

from ..models import Page


#
#   Tag Definitions
#

register = template.Library()


@register.inclusion_tag("tags/page_links.html")
def page_links():
    all_pages = Page.objects.all()
    ret = list()
    for page in all_pages:
        ret.append({'link_name': page.link_name,
                    'link': page.get_absolute_url()})
    return {'pages': ret}


@register.inclusion_tag("tags/custom_style.html")
def custom_style(filename):
    return {'custom_style': 'style/' + filename}
