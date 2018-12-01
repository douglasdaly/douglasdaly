# -*- coding: utf-8 -*-
"""
markdownify.py

    Code for markdown/pygments - based on code from www.IgnoredByDinosaurs.com

"""
#
#   Imports
#
from django import template

from douglasdaly.templatetags.markdownify import md


#
#   Filter Setup
#

register = template.Library()


@register.filter
def markdown(value):
    """ Convert markdown content to HTML
    """
    return md(value)
