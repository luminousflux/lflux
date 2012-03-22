from django.conf.urls.defaults import patterns, include, url
from feeds import StoryFeed

urlpatterns = patterns('',
    url(r'^(?P<slug>.*)/daily/$', StoryFeed('daily')),
)

