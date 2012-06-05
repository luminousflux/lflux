from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from admin_tools.dashboard.modules import DashboardModule
from admin_tools.utils import get_admin_site_name

class OwnInstancesList(DashboardModule):
    template = 'ltools/owninstances.html'
    layout = 'stacked'
    title = _('My Instances')

    def __init__(self, title, model, key='user', **kwargs):
        self.model = model
        self.key = key
        super(OwnInstancesList, self).__init__(title, **kwargs)
        self.title = model
    def __init__(self, title, model, key='user', **kwargs):
        self.model = model
        self.key = key
        super(OwnInstancesList, self).__init__(title, **kwargs)
        self.title = model

    def init_with_context(self, context):
        fltr = {}
        fltr[self.key] = context['request'].user
        children = self.model._default_manager.filter(**fltr)
        self.title = 'My %s' % self.model._meta.verbose_name_plural
        self.children = []
        for instance in children:
            self.children.append({
                'title': unicode(instance),
                'change_url': reverse('%s:%s_%s_change' % (get_admin_site_name(context),
                    self.model._meta.app_label,
                    self.model.__name__.lower(),
                    ), args=(instance.pk,))
                })

        self._initialized = True

class ModelAdd(DashboardModule):
    template = 'ltools/modeladd.html'
    layout = 'stacked'
    title = _('My Model Actions')
    show_title = False

    def __init__(self, title, model, text='Create new Instance', **kwargs):
        self.model = model
        self.text = text
        super(ModelAdd, self).__init__(title, **kwargs)

    def init_with_context(self, context):
        self.title = None
        self.children = []
        self.children.append({
            'title': self.text,
            'add_url': reverse('%s:%s_%s_add' % (get_admin_site_name(context),
                self.model._meta.app_label,
                self.model.__name__.lower(),
                ))
            })

        self._initialized = True


