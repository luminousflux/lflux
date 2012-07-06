from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.conf import settings
from ladmin.admin import admin
from django.contrib import admin as adminadmin
adminadmin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url('^story/', include('lfluxproject.lstory.urls')),
    url('^$', 'lstory.views.index'),

    url(r'^admin_tools/', include('admin_tools.urls')),
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
