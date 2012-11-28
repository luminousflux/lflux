from datetime import datetime

from django.contrib import admin
from django.db import models
import reversion

from models import Story, StorySummary

from limage.widgets import AdminPagedownWidget
from limage.models import Image
from django.contrib.contenttypes import generic


class StoryAdmin(reversion.VersionAdmin):
    prepopulated_fields = {"slug": ("name",)}
admin.site.register(Story, StoryAdmin)


class StoryUserAdmin(StoryAdmin):
    exclude = ('authors', 'tags', 'published',)

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.pk and request.user not in obj.authors.all():
            obj.authors.add(request.user)

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

        print 'publish', publish

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

            templateresponse.context_data['diff'] = story.diff_to_older(story.versions.for_date(last_summary))

        return templateresponse

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super(StorySummaryAdmin, self).save_model(request, obj, form, change)
admin.site.register(StorySummary, StorySummaryAdmin)
