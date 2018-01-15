"""
post_tags.py

    Code for Post related inclusion tags for blog.

@author: Douglas Daly
@date: 1/6/2018
"""
#
#   Imports
#
from django import template
from django.core.paginator import Paginator

from ..models import Post


#
#   Tag Definitions
#

register = template.Library()


@register.inclusion_tag("blog/tags/post_display.html")
def post_display(post):
    """ Tag to display Post Link for main Page
    """
    if post.icon_image is not None:
        img_url = "blog/media/posts/icons/" + post.icon_image
    else:
        img_url = None

    return {"post": post,
            "icon_image_url": img_url}


@register.inclusion_tag("blog/tags/post_paginator.html")
def post_pagination(post_paginator):
    """ Tag to display page links for posts
    """
    start_page = max(post_paginator.number-2, 1)
    end_page = min(post_paginator.paginator.num_pages,
                   post_paginator.number + 2) + 1

    if post_paginator.number < 3:
        end_page = min(post_paginator.paginator.num_pages, 5) + 1
    if post_paginator.number > post_paginator.paginator.num_pages - 3:
        start_page = max(post_paginator.paginator.num_pages - 4, 1)

    page_nos = range(start_page, end_page)

    return {'paginator': post_paginator,
            'page_numbers': page_nos}


@register.inclusion_tag("blog/tags/post_additional_javascript.html")
def post_additional_javascript(post_custom_script):
    """ Tag to add custom javascript to page top
    """
    if post_custom_script is not None:
        script_link = 'blog/media/posts/scripts/' + post_custom_script
    else:
        script_link = None

    return {'additional_script_link': script_link}
