# -*- coding: utf-8 -*-

import operator
import html2text
import reversion

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from ltools.models import VersionedContentMixin
from ltools.fields import CountryField
from ltools.managers import VersionManagerAccessor
from lstory.managers import StoryManager

from taggit.managers import TaggableManager
from tumblelog.models import Post


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
    body = models.TextField(_('body'), help_text=_('markdown-formatted summary text consistiong of 2 or 3 list items only!'),)

    story = models.ForeignKey(Story)
    for_revision = models.ForeignKey(reversion.models.Revision)
    revision_date = models.DateTimeField()

    author = models.ForeignKey(User)

    class Meta:
        verbose_name = _('Story Summary')
        verbose_name_plural = _('Story Summaries')
        unique_together = (('story', 'for_revision',),)

    @models.permalink
    def get_absolute_url(self):
        return ('storysummary', [self.story.slug, self.for_revision.pk],)

    def __unicode__(self):
        return u'Summary for %s at %s' % (self.story.slug, self.revision_date,)

    def story_diff(self):
        cur = self.storyversion()
        prev = cur.versions.previous()
        return cur.diff_to_older(prev)

    def storyversion(self):
        return [y for y in self.story.versions.list() if y._version.revision==self.for_revision][0]

    def previous_summary(self):
        previous_summaries = self.story.storysummary_set.filter(revision_date__lt=self.revision_date).order_by('-revision_date')
        return previous_summaries[0] if previous_summaries else None

    def tumbleposts(self):
        posts = Post.objects.filter(parent=self.story, published_at__lte=self.revision_date)
        prev = self.previous_summary()
        if prev:
            posts=posts.filter(published_at__gte=prev.revision_date)
        return posts

    @classmethod
    def summarize_period(cls, story, start_date, end_date):
        summaries = cls.objects.filter(revision_date__lte=end_date, story=story)
        if start_date:
            summaries = summaries.filter(revision_date__gte=start_date)
        posts = reduce(set.union, [set(x.tumbleposts()) for x in summaries], set())

        field_order = [('body','','\n\n',), ('source',u'—','\n',), ('title','','\n',),('text','','\n',),('photo','photo: ','\n',),('url','','\n',)]

        to_s = lambda data,field_order: ''.join([pre+data[key]+post for key,pre,post in field_order if key in data and data[key]])

        posts = [to_s(post.data,field_order) for post in posts]
        posts = [x for x in posts if x]

        return render_to_string('lstory/storysummary.txt', {'summaries': summaries, 'posts': posts})


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
