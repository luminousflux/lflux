from django.db import models
from django.contrib.comments.models import Comment
from django.contrib.auth.models import User
from lstory.models import Story
from django.utils.translation import ugettext as _

STATES = ['new', 'researching', 'answered']
STATES = [(x,x,) for x in STATES]

class Question(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    comment = models.TextField(verbose_name=_('Comment'))
    user = models.ForeignKey(User, verbose_name=_('User'))
    story = models.ForeignKey(Story, verbose_name=_('Story'))

    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)

    state = models.TextField(verbose_name=_('State'), max_length=255, choices=STATES, default=STATES[0])

    @models.permalink
    def get_absolute_url(self):
        return ('lqa_question', (), {'story_slug': self.story.slug, 'object_id': self.id},)
