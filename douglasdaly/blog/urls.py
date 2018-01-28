
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
            r'^view/(?P<slug>[^\.]+).html',
            views.view_post,
            name='view_blog_post'
    ),
    url(
            r'^categories.html',
            views.view_categories,
            name="view_blog_categories"
    ),
    url(
            r'^categories/(?P<slug>[^\.]+).html',
            views.view_category,
            name='view_blog_category'
    ),
    url(
            r'^tags.html',
            views.view_tags,
            name="view_blog_tags"
    ),
    url(
            r'^tags/(?P<slug>[^\.]+).html',
            views.view_tag,
            name='view_blog_tag'
    ),
    url(
            r'^update_sort_tab/(?P<sort_tab>[^\.]+)',
            views.update_side_menu_sort,
            name="update_side_menu_sort"
    ),
]
