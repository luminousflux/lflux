from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required
from lstory.models import Story
from limage.views import browse
from views import share

urlpatterns = patterns(
    '',
    url(r'^lstory/story/(?P<id>[^/]+)/images/$', login_required(browse), {'model': Story},
        name='ladmin_imagebrowse'),
    url(r'^lstory/story/(?P<id>[^/]+)/share/$', login_required(share), {'model': Story, 'key': 'authors'},
        name='ladmin_sharestory'),
)
