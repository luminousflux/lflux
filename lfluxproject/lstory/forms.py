from django import forms
from .models import StorySummary
from django.utils.translation import ugettext_lazy as _

class StorySummaryForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea, help_text=_('markdown-formatted summary text consistiong of 2 or 3 list items only!'))
