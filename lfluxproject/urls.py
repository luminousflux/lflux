from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.conf import settings
from lstory.models import Story
from django.contrib.auth.decorators import login_required
from limage.views import browse
from ladmin.admin import admin
from django.contrib import admin as adminadmin
adminadmin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    
    url('^story/', include('lfluxproject.lstory.urls')),
    url('^image/', include('lfluxproject.limage.urls')),
    url('^$', 'lstory.views.index'),
    
    url(r'^admin_tools/', include('admin_tools.urls')),


    url(r'^admin/lstory/story/(?P<id>[^/]+)/images/$', login_required(browse), {'model': Story},),
    url(r'^backend/', include(admin.urls)),
    url(r'^admin/', include(adminadmin.site.urls)),
)

if settings.DEMO_MODE:
    urlpatterns+=patterns('',url(r'^accounts/', include('userena.urls')),)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
