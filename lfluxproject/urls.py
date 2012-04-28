from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lfluxproject.views.home', name='home'),
    # url(r'^lfluxproject/', include('lfluxproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url('^story/', include('lfluxproject.lstory.urls')),
    url('^image/', include('lfluxproject.limage.urls')),
    url('^$', 'lstory.views.index'),
)
