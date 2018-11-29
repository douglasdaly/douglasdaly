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

from douglasdaly.models import (Asset, ImageAsset, FileAsset, VideoAsset,
                                SiteAdminSettings)


#
#   Classes
#

class HighlightRenderer(mistune.Renderer):
    """
    Renderer class for Markup
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        site_settings = SiteAdminSettings.load()
        self.DEFAULT_VIDEO_WIDTH = site_settings.default_video_width
        self.DEFAULT_VIDEO_HEIGHT = site_settings.default_video_height
        self.DEFAULT_VIDEO_AUTOPLAY = site_settings.default_video_autoplay
        self.DEFAULT_VIDEO_CONTROLS = site_settings.default_video_controls

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
        asset_slug, args = self._asset_url_helper(src)
        if asset_slug is not None:
            asset = Asset.objects.filter(slug=asset_slug).first()
            if asset is not None:
                if asset.type == "video":
                    return self.video(src, title, text)

                size = args.get('size', None)
                crop = args.get('crop', None)
                quality = args.get('quality', 99)

                asset = ImageAsset.objects.filter(slug=asset.slug).first()
                if asset is None:
                    return super().image(src, title, text)

                if size is not None:
                    image_asset = get_thumbnail(asset.asset, size,
                                                crop=crop, quality=quality)
                else:
                    image_asset = asset.asset

                src = image_asset.url
                if title is None or len(title) == 0:
                    title = asset.title
                if text is None or len(text) == 0:
                    text = asset.description
        else:
            # - Check if Video
            video_extensions = ['.mp4', '.ogg']
            if src.lower().split('.')[-1] in video_extensions:
                return self.video(src, title, text)

        return super().image(src, title, text)

    def link(self, link, title, text):
        args = HighlightRenderer._asset_url_helper(link)
        if args is not None:
            asset = FileAsset.objects.filter(slug=args[0]).first()

            if asset is not None:
                link = asset.asset.url
                if title is None or len(title) == 0:
                    title = asset.description
                if text is None or len(text) == 0:
                    text = asset.title

        return super().link(link, title, text)

    def video(self, src, title, text, video_width=None, video_height=None,
              autoplay=None, controls=None, loop=None):
        """Video html render function"""
        asset_slug, args = HighlightRenderer._asset_url_helper(src)
        if asset_slug is not None:
            asset = VideoAsset.objects.filter(slug=asset_slug).first()

            size = args.get('size', None)
            if autoplay is None:
                autoplay = args.get('autoplay', None)
                if autoplay is not None:
                    autoplay = autoplay == 'true'
            if controls is None:
                controls = args.get('controls', None)
                if controls is not None:
                    controls = controls == 'true'
            if loop is None:
                loop = args.get('loop', None)
                if loop is not None:
                    loop = loop == 'true'

            if asset is not None:
                src = asset.asset.url

                if not title:
                    title = asset.title
                if not text:
                    text = asset.description

                if autoplay is None:
                    autoplay = asset.autoplay
                if controls is None:
                    controls = asset.controls
                if loop is None:
                    loop = asset.loop

                if size is None:
                    video_width = asset.video_width
                    video_height = asset.video_height
                else:
                    try:
                        (video_width, video_height) = (int(x) for x in size.split('x'))
                    except ValueError:
                        pass

        if video_width is None:
            video_width = self.DEFAULT_VIDEO_WIDTH
        if video_height is None:
            video_height = self.DEFAULT_VIDEO_HEIGHT
        if loop is None:
            loop = False
        if controls is None:
            controls = self.DEFAULT_VIDEO_CONTROLS
        if autoplay is None:
            autoplay = self.DEFAULT_VIDEO_AUTOPLAY

        if not controls and not autoplay:
            autoplay = True

        src = mistune.escape_link(src)
        ext = src.split('.')[-1]
        if title:
            title = mistune.escape(title)
        if text:
            text = mistune.escape(text)

        # - Render
        html = '<video width="'
        if video_width:
            html += '{}" height="'.format(video_width)
        if video_height:
            html += '{}"'.format(video_height)

        if controls:
            html += " controls"
        if autoplay:
            html += " autoplay muted"
        if loop:
            html += " loop"
        html += ">"

        html += '<source src="{}" type="video/{}">'.format(src, ext)
        if title:
            html += title
            if text:
                html += ": " + text
        else:
            if text:
                html += text
            else:
                html += "Your browser does not support the video tag."
        html += "</video>"

        return html

    @staticmethod
    def _asset_url_helper(url):
        if not url.startswith("asset:"):
            return None, None

        ret = url.lower().split(':')[1:]
        slug = ret[0]
        args = dict()
        if len(ret) > 1:
            for r in ret[1:]:
                if ',' in r:
                    t_args = r.split(',')
                else:
                    t_args = [r]
                for ta in t_args:
                    if '=' in ta:
                        tspl = ta.split('=')
                        if len(tspl) == 2:
                            args[tspl[0]] = tspl[1]

        return slug, args


#
#   Filter Setup
#

register = template.Library()

renderer = HighlightRenderer()
md = mistune.Markdown(renderer=renderer)


@register.filter
def markdown(value):
    return md(value)
