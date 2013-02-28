from django.conf.urls.defaults import patterns, include, url
from .views import confirm

urlpatterns = patterns(
    '',
    url(r'^confirm/(?P<email>[^/]+)/(?P<created_at>[^/]+)/(?P<token>[^/]+)/$', confirm, name='lsubscribe_confirm'),
)
