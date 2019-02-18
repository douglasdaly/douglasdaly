# -*- coding: utf-8 -*-
"""
assets/templatetags/utils.py

    Asset app utilities

@author: Douglas Daly
@date: 1/5/2019
"""
#
#   Imports
#
import mistune
from sorl.thumbnail import get_thumbnail

from .models import Asset, ImageAsset, FileAsset, VideoAsset, AssetSettings


#
#   Variables
#

_VIDEO_EXTENSIONS = ('.mp4', '.ogg')


#
#   Classes
#

# - Markdown renderer which handles asset links

class AssetRenderer(mistune.Renderer):
    """
    Renderer class for Markdown
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        asset_settings = AssetSettings.load()
        self.DEFAULT_VIDEO_WIDTH = asset_settings.default_video_width
        self.DEFAULT_VIDEO_HEIGHT = asset_settings.default_video_height
        self.DEFAULT_VIDEO_AUTOPLAY = asset_settings.default_video_autoplay
        self.DEFAULT_VIDEO_CONTROLS = asset_settings.default_video_controls

    def image(self, src, title, text, attribute=None):
        """Image rendering for assets"""
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
                if not src:
                    src = ''
                if title is None or len(title) == 0:
                    title = asset.title
                if text is None or len(text) == 0:
                    text = asset.description
        else:
            # - Check if Video asset
            if src.lower().split('.')[-1] in _VIDEO_EXTENSIONS:
                return self.video(src, title, text, attribute=attribute)

        if not attribute:
            attribute = "image-fluid"

        # - Render image HTML
        src = mistune.escape_link(src)
        text = mistune.escape(text, quote=True)
        if title:
            title = mistune.escape(title, quote=True)
            html = '<img src="%s" alt="%s" title="%s"' % (src, text, title)
        else:
            html = '<img src="%s" alt="%s"' % (src, text)

        if attribute:
            html = '%s class="%s"' % (html, attribute)

        if self.options.get('use_xhtml'):
            return '%s />' % html
        return '%s>' % html

    def link(self, link, title, text):
        """Link render function to also handle assets"""
        args = AssetRenderer._asset_url_helper(link)
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
              autoplay=None, controls=None, loop=None, attribute=None):
        """Video html render function"""
        asset_slug, args = AssetRenderer._asset_url_helper(src)
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
                if asset.asset.url:
                    src = asset.asset.url
                else:
                    src = ''

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
        if attribute:
            html += 'class="%s"' % (attribute,)

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
        """Helper function to get properties from asset URL"""
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
#   Functions
#

def process_bulk_upload_file(bulk_file):
    """Function to process bulk upload files and return Assets"""
    pass
