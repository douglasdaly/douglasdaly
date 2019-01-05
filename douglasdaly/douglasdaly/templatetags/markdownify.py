# -*- coding: utf-8 -*-
"""
markdownify.py

    Code for markdown/pygments - based on code from www.IgnoredByDinosaurs.com

"""
#
#   Imports
#
import re
from django import template

import mistune
from mistune_contrib import math
from pygments import highlight
from pygments.util import ClassNotFound
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter

from assets.utils import AssetRenderer


#
#   Classes
#

class HighlightRenderer(AssetRenderer, math.MathRendererMixin):
    """
    Renderer class for Markdown
    """

    def math(self, text):
        return '\\(%s\\)' % text

    def block_code(self, code, lang=None):
        if not lang:
            return '\n<div class="highlight"><pre><code>' + \
                   '%s</code></pre></div>\n' % mistune.escape(code)

        try:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = HtmlFormatter(linenos="inline")
            return highlight(code, lexer, formatter)
        except ClassNotFound:
            return self.block_code(code)


class MathBlockLexer(math.MathBlockMixin, mistune.BlockLexer):
    """Block Lexer for MathJax support"""

    def __init__(self, *args, **kwargs):
        super(MathBlockLexer, self).__init__(*args, **kwargs)
        self.enable_math()


class CustomInlineLexer(mistune.InlineLexer, math.MathInlineMixin):
    """Inline Lexer for MathJax support and disabled underscores"""

    def __init__(self, *args, **kwargs):
        super(CustomInlineLexer, self).__init__(*args, **kwargs)
        self.enable_math()

        # - Customize rules
        self.rules.math = re.compile(r'^\\\((.+?)\\\)')

        self.rules.emphasis = re.compile(
            r'^\*((?:\*\*|[^\*])+?)\*(?!\*)'  # *word*
        )
        self.rules.double_emphasis = re.compile(
            r'^\*{2}([\s\S]+?)\*{2}(?!\*)'  # **word**
        )

    def output_emphasis(self, m):
        text = m.group(1)
        text = self.output(text)
        return self.renderer.emphasis(text)

    def output_double_emphasis(self, m):
        text = m.group(1)
        text = self.output(text)
        return self.renderer.double_emphasis(text)


#
#   Filter Setup
#

register = template.Library()

renderer = HighlightRenderer()
md = mistune.Markdown(renderer=renderer, inline=CustomInlineLexer,
                      block=MathBlockLexer)


@register.filter
def markdown(value):
    return md(value)
