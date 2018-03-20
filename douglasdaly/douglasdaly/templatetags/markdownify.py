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
from sorl.thumbnail import get_thumbnail

from douglasdaly.models import ImageAsset


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

    def image(self, src, title, text):
        if src.startswith('asset:'):
            args = src.split(':')
            asset_slug = args[1]
            asset = ImageAsset.objects.filter(slug=asset_slug).first()

            if asset is None:
                return super().image(src, title, text)

            size = None
            crop = None
            quality = 99
            if len(args) > 2:
                size = args[2]
            if len(args) > 3:
                crop = args[3]
            if len(args) > 4:
                quality = int(args[4])

            if size is not None:
                image_asset = get_thumbnail(asset.asset, size, crop=crop, quality=quality)
            else:
                image_asset = asset.asset

            src = image_asset.url
            if title is None or len(title) == 0:
                title = asset.title

            if text is None or len(text) == 0:
                text = asset.description

        return super().image(src, title, text)


#
#   Filter Setup
#

register = template.Library()


@register.filter
def markdown(value):
    md = mistune.Markdown(renderer=HighlightRenderer())
    return md(value)
