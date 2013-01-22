from django.contrib.auth.models import User
from django.contrib.admin import AdminSite
from lstory.admin import Story, StoryUserAdmin, ChangeSuggestion, ChangeSuggestionAdmin, StorySummary, StorySummaryAdmin, Stakeholder, StakeholderAdmin, BackgroundContent, BackgroundContentAdmin
from urls import urlpatterns
from django import forms
from tumblelog.admin import admin_classes
from django.contrib.flatpages.admin import FlatPage, FlatPageAdmin


class UserShareForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_staff=True),
                                           label='Share with', required=False)

    def __init__(self, current_user, *args, **kwargs):
        self.base_fields['users'].queryset = self.base_fields['users'].queryset.exclude(pk=current_user.pk)
        super(UserShareForm, self).__init__(*args, **kwargs)


class UserBasedStoryAdmin(StoryUserAdmin):
    def queryset(self, request):
        qs = super(UserBasedStoryAdmin, self).queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(authors=request.user)
        return qs
    change_form_template = 'ladmin/lstory/story/change_form.html'


class LAdminSite(AdminSite):
    def get_urls(self):
        urls = super(LAdminSite, self).get_urls()
        return  urlpatterns + urls


admin = LAdminSite('backend')
admin.register(Stakeholder, StakeholderAdmin)
admin.register(Story, UserBasedStoryAdmin)
admin.register(StorySummary, StorySummaryAdmin)
admin.register(ChangeSuggestion, ChangeSuggestionAdmin)
admin.register(BackgroundContent, BackgroundContentAdmin)
admin.register(FlatPage, FlatPageAdmin)

for admin_class in admin_classes:
    model, cls = admin_class
    newcls = type(cls.__name__+'ForUser',
            (cls,object,),
            {'has_add_permission': lambda self, request: True,
             'has_change_permission': lambda self, request, obj=None: True if not obj else obj.author==request.user,
             'has_delete_permission': lambda self, request, obj=None: True if not obj else obj.author==request.user,
             'queryset': lambda self, request: super(self.__class__,self).queryset(request).filter(author=request.user)
            })
    admin.register(model, newcls)
