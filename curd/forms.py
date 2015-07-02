#!/usr/bin/env python
#-*- coding:UTF-8 -*-
from django import forms
from curd.models import Curd

class NewRecordForm(forms.ModelForm):
    class Meta:
        model=Curd
        fields=['name','email','age','homePage','isMarried']




