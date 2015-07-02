__author__ = 'wuhongbin'
from django import forms
from assets.models import AwsAccounts

class NewRecordForm(forms.ModelForm):
    class Meta:
        model=AwsAccounts
        fields=['account_id','access_key_id','access_key']
