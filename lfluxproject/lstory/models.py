from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from ltools.managers import VersionManagerAccessor
import reversion

class Story(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    last_update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(null=True)
    authors = models.ManyToManyField(User)

    timeframe_start = models.DateField(null=True)
    timeframe_end = models.DateField(null=True, blank=True)

    region = models.CharField(max_length=255)

    body = models.TextField()



    tags = TaggableManager(blank=True)

    versions = VersionManagerAccessor()

    def __unicode__(self):
        return "%s%s" % (self.title, ' /unpublished' if not self.published else '')

    class Meta:
        verbose_name_plural = 'Stories'

    def get_absolute_url(self):
        return 'bullshit!'

try:
    reversion.register(Story)
except reversion.revisions.RegistrationError, e:
    if not unicode(e).endswith('has already been registered with django-reversion'):
        raise

