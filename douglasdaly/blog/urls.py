
#
#   Imports
#
from django.conf.urls import url


#
#   Patterns
#

urlpatterns = [
    url(r'^$', 'douglasdaly.blog.views.index'),
    url(
            r'^blog/view/(?P<slug>[^\.]+).html',
            'douglasdaly.blog.views.view_post',
            name='view_blog_post'
    ),
    url(
            r'^blog/category/(?P<slug>[^\.]+).html',
            'douglasdaly.blog.views.view_category',
            name='view_blog_category'
    ),
]
