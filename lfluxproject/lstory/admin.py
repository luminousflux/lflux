from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

from django.contrib import admin
from django.db import models
import reversion

from models import Story, StorySummary, ChangeSuggestion, Stakeholder

from limage.widgets import AdminPagedownWidget
from limage.models import Image
from django.contrib.contenttypes import generic
from django import forms


class StakeholderAdmin(reversion.VersionAdmin):
    pass
admin.site.register(Stakeholder, StakeholderAdmin)

class StakeholderInline(admin.StackedInline):
    model = Stakeholder
    extra = 1


class StoryAdmin(reversion.VersionAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [StakeholderInline,]
admin.site.register(Story, StoryAdmin)


class StoryUserAdmin(StoryAdmin):
    exclude = ('authors', 'tags', 'published',)

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        s = Story.objects.get(pk=object_id)

        last_summary_date = None

        existing_summaries = s.storysummary_set.all().order_by('-timeframe_end')

        if existing_summaries:
            last_summary_date = existing_summaries[0].timeframe_end

        versions_since = s.versions.by_date().keys()
        if last_summary_date:
            versions_since = [x for x in versions_since if x >= last_summary_date.date()]


        extra_context = {'versions_since': len(versions_since),
                         'last_summary_date': last_summary_date,
                         'summaries': existing_summaries,
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

class StorySummaryAdmin(admin.ModelAdmin):
    add_form_template = 'lstory/storysummary/add_form.html'

    exclude = ('author',)

    def add_view(self, request, *args, **kwargs):
        templateresponse = super(StorySummaryAdmin, self).add_view(request, *args, **kwargs)

        if not hasattr(templateresponse, 'context_data'):
            return templateresponse

        form = templateresponse.context_data['adminform'].form

        story_id = form.initial.get('story') or form.data.get('story')

        if story_id:
            story = Story.objects.get(pk=story_id)
            summaries = story.storysummary_set.all().order_by('-timeframe_end')
            last_summary = summaries[0].timeframe_end if summaries else story.published
            if not 'timeframe_start' in form.data:
                form.initial['timeframe_start'] = last_summary
                form.initial['timeframe_end'] = datetime.now()

            older_version = None
            try:
                story.versions.for_date(last_summary)
            except ObjectDoesNotExist, e:
                l = story.versions.list()
                if l:
                    older_version = l[-1]


            templateresponse.context_data['diff'] = story.diff_to_older(older_version) if older_version else None

        return templateresponse

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super(StorySummaryAdmin, self).save_model(request, obj, form, change)
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

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        return super(ChangeSuggestionAdmin, self).save_model(request, obj, form, change)
admin.site.register(ChangeSuggestion, ChangeSuggestionAdmin)
