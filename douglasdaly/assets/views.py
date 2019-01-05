# -*- coding: utf-8 -*-
"""
assets/views.py

    Views for the Assets app

@author: Douglas Daly
@date: 1/5/2019
"""
#
#   Imports
#
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from sorl.thumbnail import get_thumbnail

from .models import FileAsset, ImageAsset


#
#   Views
#

def get_asset(request):
    slug = request.GET.get("slug", None)
    asset_type = request.GET.get("type", None)

    if asset_type == "file":
        asset = get_object_or_404(FileAsset, slug=slug)

        data = {
            'title': asset.title,
            'description': asset.description,
            'url': asset.asset.url
        }

    elif asset_type == "image":
        asset = get_object_or_404(ImageAsset, slug=slug)

        size = request.GET.get("size", None)
        crop = request.GET.get("crop", None)
        quality = request.GET.get("quality", None)

        if size == '':
            size = None
        if crop == '':
            crop = None
        if quality == '':
            quality = None

        if size is not None:
            new_im = get_thumbnail(asset.asset, size, crop=crop, quality=quality)
        else:
            new_im = asset.asset

        data = {
            'title': asset.title,
            'description': asset.description,
            'url': new_im.url
        }

    else:
        raise Http404

    return JsonResponse(data)
