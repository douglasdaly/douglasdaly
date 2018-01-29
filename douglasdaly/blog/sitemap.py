"""
Blog application Sitemap
"""
#
#   Imports
#
from django.contrib.sitemaps import Sitemap

from .models import Post


#
#   Sitemaps
#

class BlogPostsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.75

    def items(self):
        return Post.objects.all()
