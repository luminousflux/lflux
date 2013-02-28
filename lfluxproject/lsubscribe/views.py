from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.views.generic.simple import direct_to_template
from django.views.generic.edit import CreateView
from .models import Subscription
from .forms import SubscriptionEmailForm
from lstory.models import Story

class SubscribeCreateView(CreateView):
    form_class=SubscriptionEmailForm
    template_name='lsubscribe/form.html'
    extra_context = {}

    def form_valid(self, form):
        obj = form.save(commit=False)
        ctx = self.get_context_data()
        obj.content_object = self.get_context_data()['obj']
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kw = super(CreateView, self).get_form_kwargs()
        init = kw.get('initial',{})
        init.update({'content_type': ContentType.objects.get_for_model(Story), 'object_id': self.get_context_data()['obj'].pk})
        kw['initial']=init
        return kw

    def get_context_data(self, **kwargs):
        context = super(SubscribeCreateView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

    def get_success_url(self):
        ctx = self.get_context_data()
        return ctx['obj'].get_absolute_url()

def subscribe(request, obj):
    return SubscribeCreateView.as_view(extra_context={'obj': obj})(request)

def confirm(request, email, created_at, token):
    s = Subscription.objects.get(email=email, created_at=created_at)
    s.confirm(token)
    return direct_to_template(request, 'lsubscribe/post_confirm.html', {'subscription': s})
