from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
import reversion

class Story(models.Model):
    title = models.TextField()
    slug = models.SlugField(unique=True)


    last_update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(null=True)
    authors = models.ManyToManyField(User)

    timeframe_start = models.DateField(null=True)
    timeframe_end = models.DateField(null=True)

    region = models.TextField(null=True)

    tags = TaggableManager()

reversion.register(Story)

