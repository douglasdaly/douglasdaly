# -*- coding: utf-8 -*-
"""
Custom widgets for the blog interface

:author: Douglas Daly
:date: 2/16/2019
"""
#
#   Imports
#
from django import forms


#
#   Custom widget classes
#

class DataAttributeSelectWidget(forms.Select):
    """
    Select widget to customize select options in admin based on given
    data to use for attributes.
    """

    def __init__(self, attrs=None, choices=(), allow_multiple_selected=False,
                 data=None):
        self.data = data if data is not None else {}
        self.allow_multiple_selected = allow_multiple_selected
        super(DataAttributeSelectWidget, self).__init__(attrs=attrs,
                                                        choices=choices)

    def create_option(self, name, value, label, selected, index, subindex=None,
                      attrs=None):
        """Create option override to show colors"""
        option = super(DataAttributeSelectWidget, self).create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        for data_attr, values, in self.data.items():
            option['attrs'][data_attr] = values[option['value']]
        return option
