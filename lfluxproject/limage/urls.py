from django.conf.urls.defaults import patterns, include, url

from views import browse

urlpatterns = patterns('',
    url(r'^$', browse,{}, 'limage-browse'),
)

