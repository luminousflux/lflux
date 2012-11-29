from django.conf import settings  # import the settings file
from django.contrib.sites.models import Site


def settings_processor(request):
    return {'settings': settings}


def tracking_processor(request):
    return {'tracking_allowed': 'do_not_track' not in request.COOKIES}


def site_processor(request):
    return {'site': Site.objects.get_current()}
