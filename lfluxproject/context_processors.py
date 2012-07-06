from django.conf import settings # import the settings file

def settings_processor(request):
    return {'settings': settings}

def tracking_processor(request):
    return {'tracking_allowed': 'do_not_track' not in request.COOKIES}
