from django import forms
from lqa.models import Question
from userena.forms import EditProfileForm as OldEditProfileForm

class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ['state', 'user', 'story']

class EditProfileForm(OldEditProfileForm):
    class Meta:
        exclude = ['_api_key', 'privacy', 'user',]
        model = OldEditProfileForm._meta.model
