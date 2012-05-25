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
    exclude = ('authors',)

    formfield_overrides = {
            models.TextField: {'widget': AdminPagedownWidget },
            }

    inlines = (ImageInline,)

    def save_model(self, request, obj, form, change):
        if obj.pk and request.user not in obj.authors.all():
            obj.authors.add(request.user)
        obj.save()
admin.site.register(Story, StoryAdmin)


class StoryUserAdmin(StoryAdmin):
    exclude = ('authors','last_update','created','published','timeframe_start','timeframe_end','region',)

