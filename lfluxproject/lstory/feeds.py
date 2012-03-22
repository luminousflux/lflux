from ltools.feeds import RevisionFeed
from models import Story
import markdown

class StoryFeed(RevisionFeed):
    def __init__(self, stype):
        super(StoryFeed, self).__init__(Story, stype)
    def get_object(self, request, slug):
        return Story.objects.get(slug=slug,published__isnull=False)
    def link(self, obj):
        return obj.get_absolute_url()
    def title(self, obj):
        return obj.title
    def item_title(self, obj):
        return '%s as of %s' % (obj.title, obj.last_update)
    def item_description(self, obj):
        return markdown.markdown(obj.body)       # TODO highlighting.

