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
from pygments.util import ClassNotFound
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from sorl.thumbnail import get_thumbnail

from douglasdaly.models import ImageAsset, FileAsset


#
#   Classes
#

class HighlightRenderer(mistune.Renderer):
    """
    Renderer class for Markup
    """

    def block_code(self, code, lang=None):
        if not lang:
            return '\n<div class="highlight"><pre><code>' + \
                   '%s</code></pre></div>\n' % mistune.escape(code)
        else:
            try:
                lexer = get_lexer_by_name(lang, stripall=True)
                formatter = HtmlFormatter(linenos="inline")
                return highlight(code, lexer, formatter)
            except ClassNotFound:
                return self.block_code(code)

    def image(self, src, title, text):
        args = self._asset_url_helper(src)
        if args is not None:
            asset_slug = args[0]
            asset = ImageAsset.objects.filter(slug=asset_slug).first()

            if asset is not None:
                size = None
                crop = None
                quality = 99
                if len(args) > 1:
                    size = args[1]
                if len(args) > 2:
                    crop = args[2]
                if len(args) > 3:
                    quality = int(args[3])

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

    def link(self, link, title, text):
        args = self._asset_url_helper(link)
        if args is not None:
            asset = FileAsset.objects.filter(slug=args[0]).first()

            if asset is not None:
                link = asset.asset.url
                if title is None or len(title) == 0:
                    title = asset.description
                if text is None or len(text) == 0:
                    text = asset.title

        return super().link(link, title, text)

    def _asset_url_helper(self, url):
        if not url.startswith("asset:"):
            return None
        ret = url.split(':')
        return ret[1:]


#
#   Filter Setup
#

register = template.Library()

renderer = HighlightRenderer()
md = mistune.Markdown(renderer=renderer)


@register.filter
def markdown(value):
    return md(value)
