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
