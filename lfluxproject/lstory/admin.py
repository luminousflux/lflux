from django.contrib import admin
from django.db import models
import reversion

from models import Story

from limage.widgets import AdminPagedownWidget
from limage.models import Image
from django.contrib.contenttypes import generic


class ImageInline(generic.GenericStackedInline):
    model = Image

class StoryAdmin(reversion.VersionAdmin):
    prepopulated_fields = {"slug": ("title",)}

    formfield_overrides = {
            models.TextField: {'widget': AdminPagedownWidget },
            }

    inlines = (ImageInline,)

    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.pk and request.user not in obj.authors.all():
            obj.authors.add(request.user)
admin.site.register(Story, StoryAdmin)


class StoryUserAdmin(StoryAdmin):
    exclude = ('authors','published','timeframe_start','timeframe_end','region','tags',)
    inlines = []

