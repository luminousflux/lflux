from django.contrib.admin import AdminSite
from lstory.admin import Story, StoryAdmin

class UserBasedStoryAdmin(StoryAdmin):
    def queryset(self, request):
        qs = super(UserBasedStoryAdmin, self).queryset(request)
        qs = qs.filter(authors=request.user)
        return qs


class LAdminSite(AdminSite):
    pass

admin = LAdminSite('admin')
admin.register(Story, UserBasedStoryAdmin)

