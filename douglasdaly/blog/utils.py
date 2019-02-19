# -*- coding: utf-8 -*-
"""
Helper utilities for the blog application.

:author: Douglas Daly
:date: 2/18/2019
"""


#
#   Functions
#

def font_color_helper(background_color, light_color=None, dark_color=None):
    """Helper function to determine which font color to use"""
    light_color = light_color if light_color is not None else "#FFFFFF"
    dark_color = dark_color if dark_color is not None else "#000000"

    tmp_color = background_color.strip().strip('#')
    tmp_r = int(tmp_color[:2], 16)
    tmp_g = int(tmp_color[2:4], 16)
    tmp_b = int(tmp_color[4:], 16)

    font_color_code = dark_color if ((tmp_r * 0.299) + (tmp_g * 0.587) +
                                     (tmp_b * 0.114)) > 186 else light_color

    return font_color_code
