#!/usr/bin/env python
# -*- coding:UTF-8 -*-
from django import forms


class AwsAccountsForm(forms.Form):
    aws_access_key_id = forms.CharField(
        required=True,
        label=u"AWS_ACCESS_KEY_ID",
        error_messages={'required': 'AWS_ACCESS_KEY_ID can not be null'},
        widget=forms.TextInput(
            attrs={
                'placeholder': "AWS_ACCESS_KEY_ID",
            }
        ),
    )
    aws_secret_access_key = forms.CharField(
        required=True,
        label=u"AWS_SECRET_ACCESS_KEY",
        error_messages={'required': u'AWS_SECRET_ACCESS_KEY can not be null'},
        widget=forms.TextInput(
            attrs={
                'placeholder': "AWS_SECRET_ACCESS_KEY",
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY can not be null")
        else:
            cleaned_data = super(AwsAccountsForm, self).clean()





