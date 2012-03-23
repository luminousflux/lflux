from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from ltools.managers import VersionManagerAccessor
import reversion
import overdiff

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

    @property
    def body_pars(self):
        return self.body.replace('\r','').split('\n\n')

    def diff_to_older(self, older):
        field_diff_data = list(overdiff.overdiff(older.body_pars, self.body_pars))
        field_diffs = []

        for i in xrange(0,len(field_diff_data)):
            field_diffs.append(overdiff.selection_to_s(self.body_pars[i], field_diff_data[i], markdown=True))
        field_diff = '\n\n'.join(field_diffs)
        return field_diff


try:
    reversion.register(Story)
except reversion.revisions.RegistrationError, e:
    if not unicode(e).endswith('has already been registered with django-reversion'):
        raise

