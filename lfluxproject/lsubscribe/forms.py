from django import forms
from django.db import models
from .models import Subscription
from django.utils.translation import ugettext as _

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription

    def clean(self):
        cleaned_data = super(SubscriptionForm, self).clean()
        if not cleaned_data.get('email','') and not cleaned_data.get('user_id',''):
            raise forms.ValidationError("need either email or user!")
        return cleaned_data

class SubscriptionEmailForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['frequency', 'email', 'content_type', 'object_id']
        widgets = {
            'frequency': forms.widgets.RadioSelect(),
            'object_id': forms.widgets.HiddenInput(),
            'content_type': forms.widgets.HiddenInput(),
        }
