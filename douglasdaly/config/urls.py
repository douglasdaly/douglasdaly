"""douglasdaly URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#
#   Imports
#
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap

from blog.sitemap import BlogPostsSitemap
from douglasdaly.sitemap import PagesSitemap
from douglasdaly.views import custom_404_view, custom_500_view


#
#   Sitemaps Setup
#

sitemaps = {
    'pages': PagesSitemap(),
    'blog': BlogPostsSitemap(),
}

#
#   Special Handlers
#

handler404 = 'douglasdaly.views.custom_404_view'
handler500 = 'douglasdaly.views.custom_500_view'


#
#   Patterns
#

urlpatterns = [
    path('404/', custom_404_view),
    path('500/', custom_500_view),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', include('robots.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('blog/', include('blog.urls'), name='blog'),
    path('', include('douglasdaly.urls'), name='douglasdaly')
]

if settings.DEBUG is True:
    import debug_toolbar
    urlpatterns = [
                      url(r'^__debug__', include(debug_toolbar.urls)),
                  ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
