from datetime import datetime, timedelta
from django.contrib.syndication.views import Feed
import reversion
from reversion.models import Version

def _feed_datelist(date_to_start, date_inc):
    current_date = date_to_start
    while current_date < datetime.now():
        yield current_date
        current_date += date_inc

subscription_types = {
        'weekly': lambda obj: _feed_datelist(obj.published-timedelta(days=obj.published.weekday,hours=obj.published.hours), timedelta(days=7)),
        'daily': lambda obj: _feed_datelist(obj.published, timedelta(days=1)),
    }

class RevisionFeed(Feed):
    ''' not a fully-implemented thing, you'll want to subclass it for different models '''
    def __init__(self, model, subtype):
        if subtype not in subscription_types.keys():
            raise Exception('%s not in possible types: %s' % subtype, ','.join(subscription_types))
        self.model = model
        self.subtype = subtype

        super(Feed, self).__init__()

    def items(self, obj):
        items = []
        itemvalues = []
        last_version = None
        for date in subscription_types[self.subtype](obj):
            v = None
            try:
                v = reversion.get_for_date(obj, date).field_dict
            except Version.DoesNotExist, e:
                pass
            if v and v!=last_version:
                last_version=v
                itemvalues.append(v)
        for iv in itemvalues:
            i = self.model()
            i.__dict__.update(iv)
            items.append(i)
        return items

