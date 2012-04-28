from django.contrib import admin
from django.db import models
import reversion

from models import Story

from pagedown.widgets import AdminPagedownWidget

class StoryAdmin(reversion.VersionAdmin):
    prepopulated_fields = {"slug": ("title",)}
    exclude = ('authors',)

    formfield_overrides = {
            models.TextField: {'widget': AdminPagedownWidget },
            }

    def save_model(self, request, obj, form, change):
        if obj.pk and request.user not in obj.authors.all():
            obj.authors.add(request.user)
        obj.save()
admin.site.register(Story, StoryAdmin)
