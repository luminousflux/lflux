from django.conf import settings  # import the settings file
from django.contrib.sites.models import Site
from django.contrib.flatpages.models import FlatPage


def settings_processor(request):
    return {'settings': settings}


def tracking_processor(request):
    return {'tracking_allowed': 'do_not_track' not in request.COOKIES}


def site_processor(request):
    return {'site': Site.objects.get_current()}

def flatcontent(request):
    path_info = request.path_info
    path_info = '/'+path_info if path_info[0]!='/' else path_info
    flatpages = FlatPage.objects.filter(url__exact=path_info)
    return {'flatcontent': None if not flatpages else flatpages[0] }
