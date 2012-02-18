from django.conf.urls.defaults import patterns, include, url

from views import serve_highlighted_text
from lfluxproject.lstory.models import Story

urlpatterns = patterns('',
    url(r'^(?P<slug>.*)/$', serve_highlighted_text, {
        'model':Story,
        'field_to_diff': 'body',
        'sessionvar': 'lstory_last',
        }, name='home'),
)

