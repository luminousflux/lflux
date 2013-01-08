from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
import reversion
from ltools.models import VersionedContentMixin
from ltools.fields import CountryField

from ltools.managers import VersionManagerAccessor
from lstory.managers import StoryManager


class Story(VersionedContentMixin, models.Model):
    name = models.CharField(max_length=255, help_text='this should not change during story development')
    title = models.CharField(max_length=255, help_text='this reflects our current understanding of the topic')
    slug = models.SlugField(unique=True, help_text='based on story name')

    last_update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(null=True, blank=True)
    authors = models.ManyToManyField(User)

    timeframe_start = models.DateField(null=True)
    timeframe_end = models.DateField(null=True, blank=True)

    cover_image = models.ImageField(null=True, blank=True, upload_to='lstory')

    region = CountryField(max_length=255, blank=True, help_text='country code, if applicable (shows map in full view)')

    summary = models.TextField(help_text='markdown-formatted summary text consistiong of 2 or 3 list items only!', blank=True)
    body = models.TextField(help_text='markdown-formatted story text', blank=True)



    tags = TaggableManager(blank=True)

    objects = StoryManager()
    versions = VersionManagerAccessor()

    def __unicode__(self):
        return "%s%s" % (self.title, ' /unpublished' if not self.published else '')

    class Meta:
        verbose_name_plural = 'Stories'
        versioned_attributes = ['body:d', 'summary:d', 'region:=', 'title:=', 'cover_image:=', 'stakeholder_set:r']

    @models.permalink
    def get_absolute_url(self):
        if hasattr(self, '_version'):
            return ('story', [self.versions.current().slug],)
        else:
            return ('story', [self.slug],)

    @models.permalink
    def get_version_url(self):
        if not hasattr(self, '_version'):
            return ('story', [self.slug],) # assume this is the current version, since _version is not set
        return ('storyversion', [self.versions.current().slug, self.ltools_versiondate.isoformat()],)
    
    @models.permalink
    def get_embed_url(self):
        return ('storyembed', [self.versions.current().slug],)




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

class ChangeSuggestion(models.Model):
    summary = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)

    story = models.ForeignKey(Story)
    for_version = models.DateTimeField(null=False, auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User)

    class Meta:
        verbose_name_plural = 'Change Suggestions'

    def __unicode__(self):
        return u'Change Suggestion for "%s", created at %s' % (self.story.versions.current().slug, self.created_at,)

class Stakeholder(VersionedContentMixin, models.Model):
    image = models.ImageField(null=True, blank=True, upload_to='lstory')
    name = models.CharField(max_length=255)
    website = models.CharField(blank=True,max_length=255)
    other_contacts = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)
    weight = models.IntegerField(default=0)

    story = models.ForeignKey(Story)
    versions = VersionManagerAccessor()

    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Stakeholders'
        versioned_attributes = ['description:d','name:=','website:=','image:=']

    def __unicode__(self):
        return u'%s for %s' % (self.name, self.story,)




try:
    reversion.register(Story, follow=['stakeholder_set'])
    reversion.register(Stakeholder)
    reversion.register(ChangeSuggestion)
except reversion.revisions.RegistrationError, e:
    print unicode(e)
    if not unicode(e).endswith('has already been registered with django-reversion'):
        raise
