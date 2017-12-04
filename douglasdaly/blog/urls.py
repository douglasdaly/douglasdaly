
#
#   Imports
#
from django.conf.urls import url

from . import views


#
#   Patterns
#

urlpatterns = [
    url(r'^$', views.index),
    url(
            r'^blog/view/(?P<slug>[^\.]+).html',
            views.view_post,
            name='view_blog_post'
    ),
    url(
            r'^blog/category/(?P<slug>[^\.]+).html',
            views.view_category,
            name='view_blog_category'
    ),
]
