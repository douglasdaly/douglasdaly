
#
#   Imports
#
from django.shortcuts import render_to_response, get_object_or_404

from .models import Post, Category, Tag


#
#   Views
#

def index(request):
    return render_to_response('blog/index.html', {
        'posts': Post.objects.all()[:5],
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    })


def view_post(request, slug):
    return render_to_response('blog/view_post.html', {
        'post': get_object_or_404(Post, slug=slug),
    })


def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render_to_response('blog/view_category.html', {
        'category': category,
        'posts': Post.objects.filter(category=category)[:5],
    })


def view_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    return render_to_response('blog/view_tag.html', {
        'tag': tag,
        'posts': Post.objects.filter(tags=tag),
    })
