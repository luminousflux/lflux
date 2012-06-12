from django.contrib.auth.models import User
from django.contrib.admin import AdminSite
from lstory.admin import Story, StoryUserAdmin
from urls import urlpatterns
from django import forms

class UserShareForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), label='Share with')

    def __init__(self, current_user, *args, **kwargs):
        self.base_fields['users'].queryset = self.base_fields['users'].queryset.exclude(pk=current_user.pk)
        super(UserShareForm, self).__init__(*args, **kwargs)


class UserBasedStoryAdmin(StoryUserAdmin):
    def queryset(self, request):
        qs = super(UserBasedStoryAdmin, self).queryset(request)
        qs = qs.filter(authors=request.user)
        return qs
    change_form_template = 'ladmin/lstory/story/change_form.html'


class LAdminSite(AdminSite):
    def get_urls(self):
        urls = super(LAdminSite, self).get_urls()
        return  urlpatterns + urls

admin = LAdminSite('backend')
admin.register(Story, UserBasedStoryAdmin)

