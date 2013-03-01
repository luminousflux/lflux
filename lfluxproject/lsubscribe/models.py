import hashlib
from datetime import datetime
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from lstory.models import StorySummary

SUBSCRIPTION_TYPES = (('daily',_('daily')), ('weekly',_('weekly'),),)

class Subscription(models.Model):
    frequency = models.CharField(_('frequency'), max_length=255, choices=SUBSCRIPTION_TYPES, null=False, blank=False, default='daily')

    email = models.EmailField(_('email'), null=True)
    user = models.ForeignKey(User, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True)
    last_delivery = models.DateTimeField(null=True)

    object_id = models.PositiveIntegerField(null=True)
    content_type = models.ForeignKey(ContentType, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ['content_type','object_id','email']

    @property
    def confirmed(self):
        return self.confirmed_at

    @property
    def who(self):
        return self.email or self.user

    def __unicode__(self):
        return u'Subscription %s (%s) on %s' % (self.who, self.frequency, self.content_object)

    @property
    def confirm_token(self):
        return hashlib.md5('%s_%s_%s' % (self.email,self.object_id,str(self.created_at),)).hexdigest()

    def send_confirm_email(self):
        site = Site.objects.get_current()
        ctx = {'site_name': site.name, 'name': self.content_object.name, 'domain': site.domain, 'confirm_link': self.confirm_link()}
        send_mail(
            _('%(site_name)s: Please confirm your subscription to %(name)s')
            % ctx,
            render_to_string('lsubscribe/confirmation_email.txt', ctx),
            settings.DEFAULT_FROM_EMAIL,
            (self.email,),
        )

    def confirm(self, token):
        self.confirmed_at = datetime.now()
        self.save()

    def save(self, *args, **kwargs):
        new = not self.pk
        super(Subscription,self).save(*args,**kwargs)
        if new:
            self.send_confirm_email()

    @models.permalink
    def confirm_link(self):
        return ('lsubscribe_confirm', (), {'email': self.email, 'created_at': str(self.created_at), 'token': self.confirm_token},)

    def send_email(self):
        now = datetime.now()
        summary = StorySummary.summarize_period(self.content_object, self.last_delivery, now).strip()

        if not summary:
            print 'no updates for summary %s' % self.pk
            return

        site = Site.objects.get_current()
        ctx = {'site_name': site.name, 'name': self.content_object.name, 'domain': site.domain, 'confirm_link': self.confirm_link(), 'frequency': self.frequency}
        send_mail(
            _('%(site_name)s: %(frequency)s mail for %(name)s')
            % ctx,
            summary,
            settings.DEFAULT_FROM_EMAIL,
            (self.email,),
        )
        self.last_delivery = now
        self.save()
