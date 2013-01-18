from django.conf.urls.defaults import patterns, include, url
from feeds import StoryFeed
from models import Story
from views import diff, version, summary, mark_as_read, toggle_tracking, backgroundcontent

urlpatterns = patterns(
    '',
    url(r'^track/yes/', toggle_tracking, {'set_track': True}, name="enable_tracking",),
    url(r'^track/no/', toggle_tracking, {'set_track': False}, name="disable_tracking",),
    url(r'^(?P<slug>[^/]*)/mark_as_read/$', mark_as_read, name="mark_as_read",),
    url(r'^(?P<slug>[^/]*)/daily/$', StoryFeed('daily'), name="storyfeed",),
    url(r'^(?P<slug>[^/]*)/v/(?P<date>[^/]*)/$', version, name='storyversion'),
    url(r'^(?P<slug>[^/]*)/s/(?P<date_end>[^/]*)/$', summary, name='storysummary'),
    url(r'^(?P<slug>[^/]*)/embed/$', diff, {
        'model': Story,
        'template': 'lstory/embed.html',
        }, name='storyembed'),
    url(r'^(?P<story_slug>[^/]*)/additional/(?P<slug>[^/]*)/$', backgroundcontent, name='backgroundcontent'),
    url(r'^(?P<slug>[^/]*)/$', diff, {
        'model': Story,
        }, name='story'),
)
