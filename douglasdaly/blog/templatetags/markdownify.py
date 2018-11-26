# -*- coding: utf-8 -*-
"""
markdownify.py

    Code for markdown/pygments - based on code from www.IgnoredByDinosaurs.com

"""
#
#   Imports
#
from django import template
import mistune

from douglasdaly.templatetags.markdownify import HighlightRenderer


#
#   Filter Setup
#

register = template.Library()

md = mistune.Markdown(renderer=HighlightRenderer())


@register.filter
def markdown(value):
    """ Convert markdown content to HTML
    """
    return md(value)
