from models import Image
from django.views.generic.simple import direct_to_template
from django.template import RequestContext
from django.http import HttpResponse

import json

def browse(request, tag=None, template='limage/browse.html'):
    imgs = Image.objects.all()
    if tag:
        imgs = imgs.filter(tags__name=tag)
    imgs = [{'url': x.img.url, 'id': x.pk,} for x in imgs]
    return HttpResponse(json.dumps(imgs), mimetype="application/json")

