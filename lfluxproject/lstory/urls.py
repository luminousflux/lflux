from django.conf.urls.defaults import patterns, include, url
from feeds import StoryFeed
from models import Story
from views import serve_highlighted_text, version

urlpatterns = patterns('',
    url(r'^(?P<slug>[^/]*)/daily/$', StoryFeed('daily')),
    url(r'^(?P<slug>[^/]*)/v/(?P<date>[^/]*)/$', version,name='storyversion'),
    url(r'^(?P<slug>[^/]*)/$', serve_highlighted_text, {
        'model':Story,
        'field_to_diff': 'body',
        'sessionvar': 'lstory_%s',
        }, name='story'),
)

