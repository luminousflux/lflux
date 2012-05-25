from models import Image
from django.views.generic.simple import direct_to_template
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from forms import ImageForm

import json

def browse(request, id=None, tag=None, model=None, template='limage/browse.html'):
    imgs = Image.objects.all()
    if model:
        o = model.objects.get(id=id)
        imgs = imgs.filter(content_type=ContentType.objects.get_for_model(model), object_id=o.pk)
    if tag:
        imgs = imgs.filter(tags__name=tag)
    imgs = {'images': [{'url': x.img.url, 'id': x.pk,} for x in imgs], 'form': ImageForm().as_p()}
    return HttpResponse(json.dumps(imgs), mimetype="application/json")

