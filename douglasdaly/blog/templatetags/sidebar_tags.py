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
        categories = Category.objects.all()
        ret = dict()
        for category in categories:
            posts = Post.objects.filter(category=category)
            ret[category] = dict()
            for post in posts:
                ret[category][post.title] = post.get_absolute_url()

    elif sort_by == "tag":
        tags = Tag.objects.all()
        ret = dict()
        for tag in tags:
            posts = Post.objects.filter(tags=tag)
            ret[tag] = dict()
            for post in posts:
                ret[tag][post.title] = post.get_absolute_url()

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
    ret = dict()

    date_years = Post.objects.all().dates('posted', 'year').distinct()
    for year in date_years:
        t_year = YearHelper(year.year)
        ret[t_year] = dict()

        posts = Post.objects.filter(posted__year=year.year)
        for post in posts:
            ret[t_year][post.title] = post.get_absolute_url()

    return ret
