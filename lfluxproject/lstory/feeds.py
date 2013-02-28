from ltools.feeds import RevisionFeed
from models import Story
from ltools.templatetags.lmarkdown import lmarkdown
from django.template.loader import render_to_string
from tumblelog.models import Post

class StoryFeed(RevisionFeed):
    def __init__(self, stype):
        super(StoryFeed, self).__init__(Story, stype)

    def get_object(self, request, slug):
        return Story.objects.get(slug=slug, published__isnull=False)

    def items(self, obj):
        return obj.storysummary_set.all()

    def link(self, obj):
        return obj.get_absolute_url()

    def title(self, obj):
        return obj.name

    def item_title(self, item):
        return item.story.title

    def item_description(self, item):
        posts = Post.objects.filter(parent=item.story, published_at__lte=item.revision_date, published_at__gte=item.previous_summary().revision_date) if item.previous_summary() else []
        return lmarkdown(item.body) + '\n\n\n<br /><br /><br />' + ''.join([render_to_string(post.template, {'post': post}) for post in posts])

    def item_pubdate(self, item):
        return item.revision_date

    def item_link(self, item):
        return item.storyversion().get_version_url()
