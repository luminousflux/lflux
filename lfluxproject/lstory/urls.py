from django.conf.urls.defaults import patterns, include, url
from feeds import StoryFeed
from models import Story
from views import serve_highlighted_text

urlpatterns = patterns('',
    url(r'^(?P<slug>.*)/daily/$', StoryFeed('daily')),
    url(r'^(?P<slug>.*)/$', serve_highlighted_text, {
        'model':Story,
        'field_to_diff': 'body',
        'sessionvar': 'lstory_%s',
        }, name='story'),
)

