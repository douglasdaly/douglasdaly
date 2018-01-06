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
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter


#
#   Classes
#

class HighlightRenderer(mistune.Renderer):

    def block_code(self, code, lang=None):
        if not lang:
            return '\n<div class="highlight"><pre><code>' + \
                   '%s</code></pre></div>\n' % mistune.escape(code)
        else:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = HtmlFormatter(linenos="inline")
            return highlight(code, lexer, formatter)


#
#   Filter Setup
#

register = template.Library()


@register.filter
def markdown(value):
    md = mistune.Markdown(renderer=HighlightRenderer())
    return md(value)
