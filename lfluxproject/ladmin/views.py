from django.contrib.auth.models import User
from django.views.generic.simple import direct_to_template
from django.template.response import TemplateResponse
from django.http import Http404
from admin_tools.utils import get_admin_site_name
from django.template import RequestContext


def ladmin(request):
    pass


def share(request, id, model, key='users', template='ladmin/share/share_object.html'):
    from ladmin.admin import UserShareForm  # there's a circular reference somewhere. oops.
    obj = model.objects.get(pk=id)
    current_shares = getattr(obj, key).all()

    if not request.user.is_superuser or not request.user in current_shares:
        raise Http404()

    share_with = obj.authors.exclude(pk=request.user.pk)

    if request.POST:
        form = UserShareForm(request.user, request.POST, initial={'users': share_with})
        if form.is_valid():
            obj.authors = list(form.cleaned_data['users']) + [request.user]
            obj.save()
    else:
        form = UserShareForm(request.user, initial={'users': share_with})

    values = {
        'opts': model._meta,
        'has_change_permission': True,
        'original': obj,
        'app_label': model._meta.app_label,
        'form': form,
    }

    return TemplateResponse(request, template, values, current_app=get_admin_site_name(RequestContext(request)))
