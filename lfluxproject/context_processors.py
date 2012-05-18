from django.conf import settings # import the settings file

def settings_processor(context):
    return {'settings': settings}

