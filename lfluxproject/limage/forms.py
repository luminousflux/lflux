from django.forms import ModelForm
from django import forms
from models import Image
from django.contrib.contenttypes.models import ContentType


class ImageForm(ModelForm):
    object_id = forms.IntegerField(widget=forms.HiddenInput())
    content_type = forms.ModelChoiceField(ContentType.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Image
        exclude = ('tags', )
