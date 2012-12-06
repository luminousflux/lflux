from django.core.http import HttpResponse

import markdown

def preview(request):
    text = request.POST['text']
    md = markdown.Markdown(extensions=['extra','insparagraph','inmoredetail'])
    return HttpResponse(md.convert(text))
