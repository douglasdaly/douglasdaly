"""
sidebar_tags.py

    Code for sidebar navigation inclusion tags for blog.

@author: Douglas Daly
@date: 1/4/2018
"""
#
#   Imports
#
from django import template

from ..models import Post, Category, Tag


#
#   Tag Definitions
#

register = template.Library()


@register.inclusion_tag("blog/tags/sidebar_menu.html")
def sidebar_menu(sort_by="date"):
    if sort_by == "date":
        ret = __sidebar_menu_helper_date()

    elif sort_by == "category":
        categories = Category.objects.all().order_by('name')
        ret = list()
        for category in categories:
            posts = Post.objects.filter(category=category).order_by('title')
            if len(posts) <= 0:
                continue
            
            temp = list()
            for post in posts:
                temp.append((post.title, post.get_absolute_url()))
            ret.append((category, temp))

    elif sort_by == "tag":
        tags = Tag.objects.all().order_by('name')
        ret = list()
        for tag in tags:
            posts = Post.objects.filter(tags=tag).order_by('title')
            if len(posts) <= 0:
                continue

            temp = list()
            for post in posts:
                temp.append((post.title, post.get_absolute_url()))
            ret.append((tag, temp))

    else:
        ret = None

    return {"sidemenu_dict": ret}


#
#   Helper Functions
#

class YearHelper(object):

    def __init__(self, year):
        self.name = str(year)
        self.slug = "Y" + str(year)


def __sidebar_menu_helper_date():
    ret = list()

    date_years = Post.objects.all().dates('posted', 'year').distinct()
    for year in date_years:
        posts = Post.objects.filter(posted__year=year.year).order_by("-posted")
        if len(posts) <= 0:
            continue

        t_year = YearHelper(year.year)
        temp = list()
        for post in posts:
            temp.append((post.title, post.get_absolute_url()))
        ret.append((t_year, temp))

    return ret
