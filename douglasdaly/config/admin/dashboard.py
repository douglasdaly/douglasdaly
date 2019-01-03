# -*- coding: utf-8 -*-
"""
config/admin/dashboard.py

    Customized jet dashboard for Django Admin

@author: Douglas Daly
@date: 12/1/2018
"""
#
#   Imports
#
from django.utils.translation import ugettext_lazy as _

from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard
from jet.dashboard.dashboard_modules import google_analytics

from .settings import JET_MODULE_GOOGLE_ANALYTICS_CLIENT_SECRETS_FILE


#
#   Classes
#

class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)

        # - Common Tasks
        self.children.append(modules.LinkList(
            _('Links'),
            children=[
                {
                    'title': _('Google Analytics'),
                    'url': 'https://www.google.com/analytics/web/?hl=en-US',
                    'external': True
                },
            ],
            column=0,
            order=0
        ))

        # - Google Analytics Charts
        if JET_MODULE_GOOGLE_ANALYTICS_CLIENT_SECRETS_FILE:
            self.children.append(
                google_analytics.GoogleAnalyticsVisitorsTotals
            )
            self.children.append(
                google_analytics.GoogleAnalyticsVisitorsChart
            )
            self.children.append(
                google_analytics.GoogleAnalyticsPeriodVisitors
            )

        # - Application Stuff
        self.children.append(modules.AppList(
            _('Applications'),
            column=1,
            order=0
        ))

        # - Misc Functions
        self.children.append(modules.LinkList(
            _('Support'),
            children=[
                {
                    'title': _('Django documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Django "django-users" mailing list'),
                    'url': 'http://groups.google.com/group/django-users',
                    'external': True,
                },
                {
                    'title': _('Django irc channel'),
                    'url': 'irc://irc.freenode.net/django',
                    'external': True,
                },
            ],
            column=2,
            order=0
        ))
