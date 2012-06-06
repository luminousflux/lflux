from django.contrib.admin import AdminSite
from lstory.admin import Story, StoryUserAdmin

class UserBasedStoryAdmin(StoryUserAdmin):
    def queryset(self, request):
        qs = super(UserBasedStoryAdmin, self).queryset(request)
        qs = qs.filter(authors=request.user)
        return qs


class LAdminSite(AdminSite):
    pass

admin = LAdminSite('backend')
admin.register(Story, UserBasedStoryAdmin)

