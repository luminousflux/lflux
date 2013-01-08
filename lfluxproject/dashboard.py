"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'lfluxproject.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'lfluxproject.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name

from lfluxproject.lstory.models import Story, ChangeSuggestion
from lfluxproject.ltools.admin import OwnInstancesList, ModelAdd, CreateForInstance
from tumblelog.bookmarklet import generate_bookmarklink


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for lfluxproject.
    """
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        # append a link list module for "quick links"

        self.children.append(OwnInstancesList(_('My Stories'), model=Story, key='authors'))
        self.children.append(modules.AppList(title='Tumblelog', models=('tumblelog.*',)))
        self.children.append(ModelAdd(None, model=Story, text='Create new Story'))
        self.children.append(OwnInstancesList(_('My Suggestions'), model=ChangeSuggestion, key='user'))
        self.children.append(CreateForInstance(model=ChangeSuggestion, instances=Story.objects.all(), key='story'))
        self.children.append(modules.LinkList('bookmarklet', children=[{'title': 'luminous flux bookmarklet', 'url': generate_bookmarklink(context['request'])}]))
        self.children.append(modules.AppList(title='Static Content', models=('django.contrib.flatpages.*',)))




class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for lfluxproject.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
