from django.db import models
from taggit.managers import TaggableManager

class Image(models.Model):
    img = models.ImageField(upload_to='limage')

    tags = TaggableManager(blank=True)

