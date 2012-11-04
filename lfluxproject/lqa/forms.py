from django import forms
from lqa.models import Question

class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ['state', 'user', 'story']
