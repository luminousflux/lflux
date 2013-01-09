from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from lstory.models import Story, ChangeSuggestion
from limage.views import browse
from views import share

urlpatterns = patterns(
    '',
    url(r'^lstory/story/(?P<id>[^/]+)/images/$', login_required(browse), {'model': Story},
        name='ladmin_imagebrowse'),
    url(r'^lstory/story/(?P<id>[^/]+)/share/$', login_required(share), {'model': Story, 'key': 'authors'},
        name='ladmin_sharestory'),
    url(r'^auth/user/(?P<id>[^/]+)/images/$', login_required(browse), {'model': User},
        name='ladmin_user_imagebrowse'),
)
