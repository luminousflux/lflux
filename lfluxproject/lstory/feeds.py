from ltools.feeds import RevisionFeed
from models import Story
from ltools.templatetags.lmarkdown import lmarkdown

class StoryFeed(RevisionFeed):
    def __init__(self, stype):
        super(StoryFeed, self).__init__(Story, stype)

    def get_object(self, request, slug):
        return Story.objects.get(slug=slug, published__isnull=False)

    def items(self, obj):
        items = [y[-1] for (x,y,) in obj.versions.by_date().iteritems()]
        return zip(items[0:-2], items[1:-1])


    def link(self, obj):
        return obj.get_absolute_url()

    def title(self, obj):
        return obj.name

    def item_title(self, item):
        prev, cur = item
        return '%s as of %s' % (cur.title, cur.last_update)

    def item_description(self, item):
        prev, cur = item
        if prev:
            diffs = cur.diff_to_older(prev)
            return lmarkdown(diffs['summary'][0]) + u'<hr />' + lmarkdown(diffs['body'][0])
        return lmarkdown(cur.body)       # TODO highlighting

    def item_pubdate(self, item):
        prev, cur = item
        return cur.last_update

    def item_link(self, item):
        prev, cur = item
        return cur.versions.current().get_absolute_url()+'#for:'+cur.last_update.isoformat()
