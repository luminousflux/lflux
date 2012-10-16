from models import Image
from django.views.generic.simple import direct_to_template
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt
from forms import ImageForm

import json


@csrf_exempt
def browse(request, id=None, tag=None, model=None, admin_instance=None, template='limage/browse.html'):
    imgs = Image.objects.all()
    o = None
    formargs = {}

    try:
        int(id)
    except ValueError:
        return HttpResponse(json.dumps({
            'form': 'sorry, we can not upload images until you saved your Story at least once!',
            'images': [],
            'enable_upload': False
        }), mimetype='application/json')

    if model:
        o = model.objects.get(id=id)
        formargs = dict(content_type=ContentType.objects.get_for_model(model), object_id=o.pk)
        imgs = imgs.filter(**formargs)
    if tag:
        imgs = imgs.filter(tags__name=tag)

    if formargs.get('content_type'):
        formargs['content_type'] = formargs['content_type'].pk

    form = ImageForm(initial=formargs)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, initial=formargs)

        if form.is_valid():
            form.save()

    imgs = {'images': [{'url': x.img.url, 'id': x.pk, } for x in imgs], 'form': form.as_p(), 'enable_upload': True}
    return HttpResponse(json.dumps(imgs), mimetype="application/json")
