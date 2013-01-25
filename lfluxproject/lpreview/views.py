from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ltools.templatetags.lmarkdown import lmarkdown

@csrf_exempt
def preview(request):
    text = request.POST['text']
    return HttpResponse(lmarkdown(text))
