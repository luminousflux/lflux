import reversion
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


from taggit.managers import TaggableManager

from ltools.models import VersionedContentMixin
from ltools.fields import CountryField
from ltools.managers import VersionManagerAccessor
from lstory.managers import StoryManager


class Story(VersionedContentMixin, models.Model):
    name = models.CharField(_('name'), max_length=255, help_text=_('this should not change during the story\'s lifetime'))
    title = models.CharField(_('title'), max_length=255, help_text=_('this reflects our current understanding of the topic'))
    slug = models.SlugField(_('slug'), unique=True, help_text=_('based on story name'))

    last_update = models.DateTimeField(_('last update'), auto_now=True)
    created = models.DateTimeField(_('created at'), auto_now_add=True)
    published = models.DateTimeField(_('published at'), null=True, blank=True)
    authors = models.ManyToManyField(User)

    timeframe_start = models.DateField(_('start of timeframe'), null=True)
    timeframe_end = models.DateField(_('end of timeframe'), null=True, blank=True)

    cover_image = models.ImageField(_('cover image'), null=True, blank=True, upload_to='lstory')

    region = CountryField(_('region'), max_length=255, blank=True, help_text=_('country code, if applicable (shows map in full view)'))

    summary = models.TextField(_('summary'), help_text=_('markdown-formatted summary text consistiong of 2 or 3 list items only!'), blank=True)
    body = models.TextField(_('body'), help_text=_('markdown-formatted story text'), blank=True)



    tags = TaggableManager(blank=True)

    objects = StoryManager()
    versions = VersionManagerAccessor()

    def __unicode__(self):
        return "%s%s" % (self.title, ' /unpublished' if not self.published else '')

    class Meta:
        verbose_name = _('Story')
        verbose_name_plural = _('Stories')
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
        s = self.versions.current().slug
        return ('storyversion', [s, self.ltools_versiondate.isoformat()],)

    @models.permalink
    def get_embed_url(self):
        return ('storyembed', [self.versions.current().slug],)


class StorySummary(models.Model):
    story = models.ForeignKey(Story)
    timeframe_start = models.DateTimeField(_('start of timeframe'))
    timeframe_end = models.DateTimeField(_('end of timeframe'))
    body = models.TextField(_('body'), help_text='markdown-formatted summary text')
    author = models.ForeignKey(User)

    class Meta:
        verbose_name = _('Story Summary')
        verbose_name_plural = _('Story Summaries')
        unique_together = (('story', 'timeframe_end',),)

    @models.permalink
    def get_absolute_url(self):
        return ('storysummary', [self.story.slug, self.timeframe_end.isoformat()],)

    def __unicode__(self):
        return u'Summary for %s between %s and %s' % (self.story.slug, self.timeframe_start, self.timeframe_end,)

    def storyversions(self):
        return self.story.versions.for_date(self.timeframe_start), self.story.versions.for_date(self.timeframe_end)

class ChangeSuggestion(models.Model):
    summary = models.TextField(_('summary'), null=True, blank=True)
    body = models.TextField(_('body'), null=True, blank=True)

    story = models.ForeignKey(Story)
    for_version = models.DateTimeField(_('for version'), null=False, auto_now_add=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    user = models.ForeignKey(User)

    class Meta:
        verbose_name = _('Change Suggestion')
        verbose_name_plural = _('Change Suggestions')

    def __unicode__(self):
        return u'Change Suggestion for "%s", created at %s' % (self.story.versions.current().slug, self.created_at,)

class Stakeholder(VersionedContentMixin, models.Model):
    image = models.ImageField(_('image'), null=True, blank=True, upload_to='lstory')
    name = models.CharField(_('name'), max_length=255)
    website = models.CharField(_('website'), blank=True,max_length=255)
    other_contacts = models.CharField(_('other contacts'), blank=True, max_length=255)
    description = models.TextField(_('description'), blank=True)
    weight = models.IntegerField(_('weight'), default=0)

    story = models.ForeignKey(Story)
    versions = VersionManagerAccessor()

    objects = models.Manager()

    class Meta:
        verbose_name = _('Stakeholder')
        verbose_name_plural = _('Stakeholders')
        versioned_attributes = ['description:d','name:=','website:=','image:=','weight:=']
        ordering = ['-weight']

    def __unicode__(self):
        return u'%s for %s' % (self.name, self.story,)


class BackgroundContent(models.Model):
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255)
    body = models.TextField(_('body'))
    weight = models.IntegerField(_('weight'), default=0)

    author = models.ForeignKey(User)
    story = models.ForeignKey(Story)

    class Meta:
        verbose_name = _('Background Content')
        verbose_name_plural = _('Background Content')

    def __unicode__(self):
        return u'%s for %s' % (self.name, self.story.name,)

    @models.permalink
    def get_absolute_url(self):
        return ('backgroundcontent', [], {'story_slug': self.story.slug, 'slug': self.slug},)



try:
    reversion.register(Story, follow=['stakeholder_set'])
    reversion.register(Stakeholder)
    reversion.register(ChangeSuggestion)
except reversion.revisions.RegistrationError, e:
    print unicode(e)
    if not unicode(e).endswith('has already been registered with django-reversion'):
        raise
