from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from ltools.managers import VersionManagerAccessor
import reversion
import overdiff
from ltools.markdowntools import pars_to_blocks

class Story(models.Model):
    title = models.CharField(max_length=255, help_text='story title')
    slug = models.SlugField(unique=True, help_text='named for the story')

    last_update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(null=True)
    authors = models.ManyToManyField(User)

    timeframe_start = models.DateField(null=True)
    timeframe_end = models.DateField(null=True, blank=True)

    region = models.CharField(max_length=255)

    body = models.TextField(help_text='markdown-formatted story text')



    tags = TaggableManager(blank=True)

    versions = VersionManagerAccessor()

    def __unicode__(self):
        return "%s%s" % (self.title, ' /unpublished' if not self.published else '')

    class Meta:
        verbose_name_plural = 'Stories'

    @models.permalink
    def get_absolute_url(self):
        return ('story', [self.slug],)

    @models.permalink
    def get_version_url(self):
        if not hasattr(self, '_version'):
            return ('story', [self.slug],)
        return ('storyversion', [self.slug, self.ltools_versiondate.isoformat()],)

    @property
    def body_pars(self):
        tmp = self.body.replace('\r','').split('\n\n')
        tmp2 = pars_to_blocks(tmp)
        return tmp2

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


class StorySummary(models.Model):
    story = models.ForeignKey(Story)
    timeframe_start = models.DateTimeField()
    timeframe_end = models.DateTimeField()
    body = models.TextField(help_text='markdown-formatted summary text')
    author = models.ForeignKey(User)

    class Meta:
        unique_together = (('story', 'timeframe_end',),)

    @models.permalink
    def get_absolute_url(self):
        return ('storysummary', [self.story.slug, self.timeframe_end.isoformat()],)

    def __unicode__(self):
        return u'Summary for %s between %s and %s' % (self.story.slug, self.timeframe_start, self.timeframe_end,)

    def storyversions(self):
        return self.story.versions.for_date(self.timeframe_start), self.story.versions.for_date(self.timeframe_end)

