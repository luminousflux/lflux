from django.db import models
from django.contrib.comments.models import Comment
from django.contrib.auth.models import User
from lstory.models import Story

STATES = ['new', 'researching', 'answered']
STATES = [(x,x,) for x in STATES]

class Question(models.Model):
    title = models.CharField(max_length=255)
    comment = models.TextField()
    user = models.ForeignKey(User)
    story = models.ForeignKey(Story)

    created_at = models.DateTimeField(auto_now_add=True)

    state = models.TextField(max_length=255, choices=STATES, default=STATES[0])

    @models.permalink
    def get_absolute_url(self):
        return ('lqa_question', (), {'story_slug': self.story.slug, 'object_id': self.id},)
