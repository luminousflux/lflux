from django.contrib import admin
import reversion
from models import Story

class StoryAdmin(reversion.VersionAdmin):
    prepopulated_fields = {"slug": ("title",)}
    exclude = ('authors',)

    def save_model(self, request, obj, form, change):
        if obj.pk and request.user not in obj.authors.all():
            obj.authors.add(request.user)
        obj.save()
admin.site.register(Story, StoryAdmin)
