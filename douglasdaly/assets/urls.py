# -*- coding: utf-8 -*-
"""
assets/urls.py

    URL configuration for assets app

@author: Douglas Daly
@date: 1/5/2019
"""
#
#   Imports
#
from django.conf.urls import url
from .views import get_asset


#
#   URL Patterns
#

urlpatterns = [
    url(r'^get_asset/$', get_asset, name="get_asset"),
]
