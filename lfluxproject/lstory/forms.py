from django import forms
from .models import StorySummary

class StorySummaryForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea)
