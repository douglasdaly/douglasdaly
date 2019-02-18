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
#   Mixin classes
#

class DataAttributeOptionMixin(object):
    """
    Mixin class for adding attributes to choices
    """

    def __init__(self, *args, data=None, **kwargs):
        self._data = data if data is not None else {}
        super(DataAttributeOptionMixin, self).__init__(*args, **kwargs)

    def create_option(self, name, value, label, selected, index, subindex=None,
                      attrs=None):
        """Create option override to show colors"""
        option = super(DataAttributeOptionMixin, self).create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )

        for data_attr, values, in self._data.items():
            if isinstance(values, dict):
                option['attrs'][data_attr] = values[option['value']]
            elif callable(values):
                option['attrs'][data_attr] = values(option['value'])

        return option


#
#   Custom form widget classes
#

class DataAttributionOptionSelectMulti(DataAttributeOptionMixin,
                                       forms.SelectMultiple):
    """
    Select widget to customize select options in admin based on given
    data to use for attributes.
    """
    pass


class ListFieldWidgetSelectMulti(DataAttributionOptionSelectMulti):
    """
    Select widget helper for list field widget
    """

    def create_option(self, name, value, label, selected, index, subindex=None,
                      attrs=None):
        """Override selected to False"""
        return super(ListFieldWidgetSelectMulti, self).create_option(
            name, value, label, False, index, subindex=subindex, attrs=attrs
        )


class ListFieldWidget(forms.Textarea):
    """
    List field with add and remove abilities
    """
    template_name = 'blog/widgets/list_field_widget.html'

    class Media:
        js = ("blog/js/list_field_widget.js",)

    def __init__(self, add_field_widget, attrs=None, can_add=True,
                 can_remove=True, add_attrs=None, list_data=None, **kwargs):
        super(ListFieldWidget, self).__init__(attrs=attrs)

        self.add_field_widget = add_field_widget
        self.add_field_kwargs = kwargs
        self.add_attrs = add_attrs if add_attrs is not None else {}
        self.list_data = list_data

        self.can_add = can_add
        self.can_remove = can_remove

    def get_context(self, name, value, attrs):
        """Override with rendering data for our add field helper"""
        ret = super(ListFieldWidget, self).get_context(name, value, attrs)

        add_name = '%s_add' % name
        list_name = '%s_list' % name

        add_obj = self.add_field_widget(**self.add_field_kwargs)
        self.add_attrs['id'] = 'id_%s' % add_name
        ret['add_field_widget_rendered'] = add_obj.render(
            add_name, value, attrs=self.add_attrs
        )

        if value:
            choices = ((x, x) for x in value)
        else:
            choices = ()

        list_obj = ListFieldWidgetSelectMulti(choices=choices,
                                              data=self.list_data)
        ret['add_list_widget_rendered'] = list_obj.render(
            list_name, value, attrs={"id": "id_%s" % list_name}
        )

        ret['can_add'] = self.can_add
        ret['can_remove'] = self.can_remove

        return ret


class ColorListFieldWidget(ListFieldWidget):
    """
    Color list field widget
    """

    def get_context(self, name, value, attrs):
        """Override to include functions"""
        ret = super(ColorListFieldWidget, self).get_context(name, value, attrs)

        ret['add_function'] = "arsAddColorValue"

        return ret
