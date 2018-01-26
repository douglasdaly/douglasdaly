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
from django.conf import settings
from django.conf.urls import url, include

from .views import index, view_page


#
#   Patterns
#

urlpatterns = [
    url(r'^$', index, name='index'),
    url('index.html', index, name='index'),
    url(r'^(?P<slug>[^\.]+).html', view_page, name='view_page'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__', include(debug_toolbar.urls)),
    ] + urlpatterns
