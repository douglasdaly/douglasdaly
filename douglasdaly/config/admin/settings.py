# -*- coding: utf-8 -*-
"""
config/admin/settings.py

    Various settings for the main Django settings regarding the admin
    customizations.

@author: Douglas Daly
@date: 12/1/2018
"""
#
#   Imports
#
import os

from django.utils.translation import ugettext_lazy as _

from ..settings.base import BASE_DIR


#
#   Jet Settings for Admin Site
#

# - Dashboards

JET_INDEX_DASHBOARD = 'config.admin.dashboard.CustomIndexDashboard'


# - Menus

JET_SIDE_MENU_ITEMS = [
    {'app_label': 'auth', 'items': [
        {'name': 'group'},
        {'name': 'user'},
    ]},
    {'app_label': 'blog', 'items': [
        {'name': 'blogsettings'},
        {'name': 'category'},
        {'name': 'customcss'},
        {'name': 'customjs'},
        {'name': 'post'},
        {'name': 'tag'},
    ]},
    {'app_label': 'douglasdaly', 'items': [
        {'name': 'fileasset'},
        {'name': 'imageasset'},
        {'name': 'page'},
        {'name': 'siteadminsettings'},
        {'name': 'sitesettings'},
        {'name': 'videoasset'},
    ]},
    {'app_label': 'robots', 'items': [
        {'name': 'rule'},
        {'name': 'url'},
    ]},
    {'app_label': 'sites', 'items': [
        {'name': 'site'},
    ]},
]


# - Themes

JET_DEFAULT_THEME = 'light-gray'

JET_THEMES = [
    {
        'theme': 'default',     # theme folder name
        'color': '#47bac1',     # color of the theme's button in user menu
        'title': 'Default'      # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    },
]

# - Additional Misc.

if "GOOGLE_CLIENT_SECRETS" in os.environ.keys():
    JET_MODULE_GOOGLE_ANALYTICS_CLIENT_SECRETS_FILE = \
        os.path.join(BASE_DIR, os.environ.get("GOOGLE_CLIENT_SECRETS"))
else:
    JET_MODULE_GOOGLE_ANALYTICS_CLIENT_SECRETS_FILE = None
