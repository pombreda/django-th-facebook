# -*- coding: utf-8 -*-

from django import forms
from django.forms import TextInput
from th_facebook.models import Facebook


class FacebookForm(forms.ModelForm):

    """
        for to handle Pocket service
    """

    class Meta:
        model = Facebook
        fields = ('title',)
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
        }


class FacebookProviderForm(FacebookForm):
    pass


class FacebookConsumerForm(FacebookForm):
    pass
