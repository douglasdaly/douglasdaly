"""
Main Sitemap
"""
#
#   Imports
#
from django.contrib.sitemaps import Sitemap

from .models import Page


#
#   Sitemaps
#

class PagesSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Page.objects.filter(published=True).all()
