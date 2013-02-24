from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ltools.templatetags.lmarkdown import lmarkdown
from django.views.generic.simple import direct_to_template

@csrf_exempt
def preview(request, template='lpreview/preview.html'):
    text = request.REQUEST['text']
    preview = lmarkdown(text)
    if not template:
        return HttpResponse(preview)
    response = direct_to_template(request, template, {'preview': preview})
    response['X-XSS-Protection'] = '0'
    return response
