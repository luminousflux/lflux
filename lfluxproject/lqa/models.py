from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_noop
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site

from django.contrib.comments.signals import comment_was_posted

import reversion

from lstory.models import Story


class Question(models.Model):
    STATES = [ugettext_noop('new'), ugettext_noop('researching'), ugettext_noop('answered'), ugettext_noop('answered in article'),]
    STATES = tuple([(x,_(x),) for x in STATES])
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    comment = models.TextField(verbose_name=_('Comment'))
    user = models.ForeignKey(User, verbose_name=_('User'))
    story = models.ForeignKey(Story, verbose_name=_('Story'))

    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)

    state = models.TextField(verbose_name=_('State'), max_length=255, choices=STATES, default=STATES[0][0])

    @models.permalink
    def get_absolute_url(self):
        return ('lqa_question', (), {'story_slug': self.story.slug, 'object_id': self.id},)

    @property
    def story_version(self):
        return self.story.versions.for_date(self.created_at)


    def notify_owner_author_answered(self, instance):
        site = Site.objects.get_current()
        ctx = {'site_name': site.name, 'name': self.story.name, 'domain': site.domain, 'question_link': self.get_absolute_url(),}
        send_mail(
            _('%(site_name)s: An Author replied to your Question on %(name)s'),
            render_to_string('lqa/author_commented_notification.txt', ctx),
            settings.DEFAULT_FROM_EMAIL,
            (self.user.email,),
        )
reversion.register(Question)


@receiver(comment_was_posted)
def send_mail_if_commented_by_author(sender, comment, request, **kwargs):
    if not comment.user:
        return

    if not hasattr(comment.content_object, 'story'):
        return

    if comment.user in comment.content_object.story.authors.all():
        comment.content_object.notify_owner_author_answered(comment)
