"""
format_tags.py

    Code for formatting various data types

@author: Douglas Daly
@date: 1/15/2018
"""
#
#   Imports
#
from django import template
from django.utils.timesince import timesince


#
#   Tag Definitions
#

register = template.Library()


@register.filter
def get_days_ago(date):
    """ Gets the Number of days from the given date to Today
    """
    ret = timesince(date)
    ret_arr = ret.split(',')[:-1]
    if len(ret_arr) >= 1:
        return ", ".join(ret_arr).strip().strip(",")
    else:
        return ret
