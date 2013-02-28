from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from functools import update_wrapper

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib import admin
from django.db import models
import reversion
from django.core.urlresolvers import reverse

from .models import Story, StorySummary, ChangeSuggestion, Stakeholder, BackgroundContent
from .forms import StorySummaryForm

from limage.widgets import AdminPagedownWidget
from limage.models import Image
from django.contrib.contenttypes import generic
from django import forms

from django.template.loader import render_to_string
from django.contrib.admin.util import unquote

from ltools.templatetags.lmarkdown import lmarkdown



from reversion.models import VERSION_CHANGE


class StakeholderAdmin(reversion.VersionAdmin):
    pass
admin.site.register(Stakeholder, StakeholderAdmin)

class StakeholderInline(admin.StackedInline):
    model = Stakeholder
    extra = 1

class StoryAdminForm(forms.ModelForm):
    class Meta:
        model = Story
    def clean_body(self):
        body = self.cleaned_data.get('body','')
        try:
            lmarkdown(body)
        except Exception, e:
            raise forms.ValidationError("syntax error in body element %s " % repr(e))
        return body
    def clean_summary(self):
        summary = self.cleaned_data.get('summary','')
        try:
            lmarkdown(summary)
        except Exception, e:
            raise forms.ValidationError("syntax error in summary element %s" % repr(e))
        return summary

class StoryAdmin(reversion.VersionAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [StakeholderInline,]
    form = StoryAdminForm
admin.site.register(Story, StoryAdmin)


class StoryUserAdmin(StoryAdmin):
    exclude = ('authors', 'tags', 'published',)

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}

        summary_form = StorySummaryForm(request.POST,prefix='storysummary') if request.POST else StorySummaryForm(prefix='storysummary')

        s = Story.objects.get(pk=object_id)


        versions_since = s.versions.by_date().keys()

        extra_context = {'versions_since': len(versions_since),
                         'changesuggestions': s.changesuggestion_set.all(),
                         'summary_form': summary_form
                         }
        publish = '_publish' in request.POST

        if publish:
            request.POST = request.POST.copy()
            request.POST['_continue'] = 1

        x = super(StoryUserAdmin, self).change_view(request, object_id,
                                                       extra_context=extra_context)

        if publish:
            s = Story.objects.get(pk=object_id)
            s.published = datetime.now()
            s.save()

        return x

    def add_view(self, request, form_url='', extra_context=None):
        request.POST = request.POST.copy()
        if '_publish' in request.POST:
            request.POST['_continue'] = request.POST['_publish']
        x = super(StoryUserAdmin, self).add_view(request, form_url, extra_context)
        return x

    def response_add(self, request, obj, *args, **kwargs):
        if '_publish' in request.POST:
            obj.published = datetime.now()
            obj.save()
        return super(StoryUserAdmin, self).response_add(request, obj, *args, **kwargs)

    def save_model(self, request, obj, form, change):
        new = not obj.pk
        r = super(StoryUserAdmin, self).save_model(request, obj, form, change)
        if new:
            obj.authors.add(request.user)
        return r

    def log_change(self, request, object, message):
        """Sets the version meta information."""
        super(reversion.VersionAdmin, self).log_change(request, object, message)
        revision = self.revision_manager.save_revision(
            self.get_revision_data(request, object, VERSION_CHANGE),
            user = request.user,
            comment = message,
            ignore_duplicates = self.ignore_duplicate_revisions,
            db = self.revision_context_manager.get_db(),
        )
        summary_form = StorySummaryForm(request.POST,prefix='storysummary')
        if summary_form.is_valid():
            body = summary_form.cleaned_data.get('body','')
            if body:
                StorySummary.objects.create(for_revision=revision, revision_date=revision.date_created, story=object, author=request.user, body=body)


class StorySummaryAdmin(admin.ModelAdmin):
    exclude = ('author',)
    add_form_template = 'lstory/storysummary/add_form.html'
    change_form_template = 'lstory/storysummary/add_form.html'

    def save_model(self, request, obj, form, change):
        new = not obj.pk
        if new:
            obj.user = request.user
        return super(ChangeSuggestionAdmin, self).save_model(request, obj, form, change)
admin.site.register(StorySummary, StorySummaryAdmin)

class ChangeSuggestionAdmin(reversion.VersionAdmin):
    add_form_template = 'lstory/changesuggestion/add_form.html'
    change_form_template = 'lstory/changesuggestion/add_form.html'
    exclude = ('user',)
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

    def _extend_view(self, templateresponse):
        if not hasattr(templateresponse, 'context_data'):
            return templateresponse

        form = templateresponse.context_data['adminform'].form

        story_id = form.initial.get('story') or form.data.get('story')

        if story_id:
            story = Story.objects.get(pk=story_id)
            version = story.versions.for_date(form.instance.for_version) if form.instance and form.instance.pk else story
            templateresponse.context_data['story_changed'] = not version.versions.is_current()
            templateresponse.context_data['original_body'] = version.body
            templateresponse.context_data['original_summary'] = version.summary
            templateresponse.context_data['current_body'] = story.body
            templateresponse.context_data['current_summary'] = story.summary
            templateresponse.context_data['story'] = story
            if (not form.instance or not form.instance.pk) and not 'body' in form.data:
                form.initial['body'] = story.body
                form.initial['summary'] = story.summary

        if not hasattr(templateresponse, 'context_data'):
            return templateresponse

        return templateresponse

    def add_view(self, request, *args, **kwargs):
        return self._extend_view(super(ChangeSuggestionAdmin, self).add_view(request, *args, **kwargs))

    def change_view(self, request, *args, **kwargs):
        return self._extend_view(super(ChangeSuggestionAdmin, self).change_view(request, *args, **kwargs))

    def save_to_story_view(self, request, object_id, *args, **kwargs):
        obj = self.get_object(request, unquote(object_id))
        story = obj.story
        if not request.user in story.authors.all():
            return HttpResponse('403')
        story.summary = obj.summary
        story.body = obj.body
        story.save()
        obj.delete()
        self.message_user(request, 'content now in story')
        return HttpResponseRedirect(reverse('backend:lstory_story_change', args=[story.pk]))

    def get_urls(self):
        urls = list(super(ChangeSuggestionAdmin, self).get_urls())
        from django.conf.urls import patterns, url
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)
        info = self.model._meta.app_label, self.model._meta.module_name
        urls1 = patterns('', 
                url(r'^([^/]+)/save_to_story/$', wrap(self.save_to_story_view), name='%s_%s_save_to_story' % info,),
            )
        return urls[0:2] + urls1 + urls[3:]

    def save_model(self, request, obj, form, change):
        new = not obj.pk
        if new:
            obj.user = request.user
        result = super(ChangeSuggestionAdmin, self).save_model(request, obj, form, change)
        if request.user not in obj.story.authors.all():
            for author in obj.story.authors.all():
                author.email_user(
                        ('new' if new else 'changed') + ' change suggestion for %s' % obj.story.name,
                        render_to_string('lstory/changesuggestion/email_to_authors.txt',
                            {'story': obj.story,
                             'changesuggestion': obj,
                             'user': request.user,
                             'recipient': author,
                             'new': new,
                             'domain': request.META['SERVER_NAME']})
                        )
        return result
admin.site.register(ChangeSuggestion, ChangeSuggestionAdmin)

class BackgroundContentAdmin(admin.ModelAdmin):
    add_form_template = 'lstory/backgroundcontent/add_form.html'
    change_form_template = 'lstory/backgroundcontent/add_form.html'
    meta = BackgroundContent
    exclude = ('author',)

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

    def has_change_permission(self, request, obj=None):
        return (request.user in obj.story.authors.all()) if obj else True

    def _extend_view(self, templateresponse):
        if not hasattr(templateresponse, 'context_data'):
            return templateresponse
        form = templateresponse.context_data['adminform'].form
        story_id = form.initial.get('story') or form.data.get('story')
        templateresponse.context_data['story_id'] = story_id
        return templateresponse


    def add_view(self, request, *args, **kwargs):
        return self._extend_view(super(BackgroundContentAdmin, self).add_view(request, *args, **kwargs))

    def change_view(self, request, *args, **kwargs):
        return self._extend_view(super(BackgroundContentAdmin, self).change_view(request, *args, **kwargs))

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super(BackgroundContentAdmin, self).save_model(request, obj, form, change)


admin.site.register(BackgroundContent, BackgroundContentAdmin)
