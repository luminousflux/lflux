from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import markdown

@csrf_exempt
def preview(request):
    text = request.POST['text']
    md = markdown.Markdown(extensions=['extra','insparagraph','inmoredetail'])
    return HttpResponse(md.convert(text))
