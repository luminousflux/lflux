from django.db import models
from tumblelog.models import Post
from tumblelog.managers import PostManager

class LPostManager(PostManager):
    def for_story(self, story):
        return self.get_query_set().filter(story=story)

class LPost(Post):
    objects = LPostManager()

    class Meta:
        proxy = True
