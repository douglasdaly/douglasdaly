"""
Code for sidebar navigation inclusion tags for blog.

:author: Douglas Daly
:date: 1/4/2018
"""
#
#   Imports
#
from django import template

from ..models import Post, Category, Tag, Author


#
#   Tag Definitions
#

register = template.Library()


@register.inclusion_tag("blog/tags/sidebar_menu.html")
def sidebar_menu(sort_by="date"):
    """Tag for side menu links"""
    heading_objects = True

    if sort_by == "date":
        ret = __sidebar_menu_helper_date()

    elif sort_by == "categories":
        categories = Category.objects.all()
        all_posts = Post.get_displayable()

        ret = list()
        for category in categories:
            posts = all_posts.filter(category=category).order_by('title')
            if len(posts) <= 0:
                continue
            
            temp = list()
            for post in posts:
                temp.append((post.title, post.get_absolute_url()))
            ret.append((category, temp))

    elif sort_by == "tags":
        heading_objects = False

        all_tags = Tag.objects.all()
        all_posts = Post.get_displayable()

        ret = list()
        letters = all_tags.values_list("_category", flat=True).distinct()
        for letter in letters:
            tags = all_tags.filter(_category=letter)
            temp = list()
            for tag in tags:
                has_posts = all_posts.filter(tags=tag).exists()
                if not has_posts:
                    continue
                temp.append((tag.name, tag.get_absolute_url()))

            if temp:
                ret.append((letter, temp))

    elif sort_by == "authors":
        heading_objects = False

        ret = list()
        all_authors = Author.get_displayable()
        for author in all_authors:
            posts = author.get_all_posts()
            if len(posts) <= 0:
                continue

            temp = list()
            for post in posts:
                temp.append((post.title, post.get_absolute_url()))
            ret.append((author.get_display_name(), temp))

    else:
        ret = None

    return {
        "sidemenu_sort": sort_by,
        "sidemenu_dict": ret,
        "sidemenu_heading_objects": heading_objects,
    }


@register.filter(is_safe=True)
def smallnavbtn(target_nav, current_nav):
    """Tag for small nav items"""
    if current_nav is not None and target_nav == current_nav:
        return "btn-primary"
    return "btn-secondary"


#
#   Helper Functions
#

class YearHelper(object):
    """
    Small helper object for displaying posts by year
    """

    def __init__(self, year):
        self.name = str(year)
        self.slug = "Y" + str(year)


def __sidebar_menu_helper_date(previews=False):
    """Helper to get all posts by year"""
    ret = list()

    all_posts = Post.get_displayable(previews=previews)
    date_years = all_posts.dates('display_date', 'year').distinct()
    for year in reversed(date_years):
        posts = all_posts.filter(published=True, posted__year=year.year)
        if len(posts) <= 0:
            continue

        t_year = YearHelper(year.year)
        temp = list()
        for post in posts:
            temp.append((post.title, post.get_absolute_url()))
        ret.append((t_year, temp))

    return ret
