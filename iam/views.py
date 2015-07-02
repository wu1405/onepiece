#!/usr/bin/env python
#-*- coding:UTF-8 -*-
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from assets.models import AwsAccounts
from iam.forms import NewRecordForm


def DeleteKey(request):
    if request.method == 'GET':
        account_del = request.GET.get('account')
        if account_del:
            data = AwsAccounts.objects.get(account_id = account_del)
            data.delete()
            message = 'account_id: %s has been deleted' % account_del
            return ShowKey(request,message)

def CreateKey(request):
    if request.method == 'GET':
        title="Add New Key"
        form = NewRecordForm()
        return render_to_response('iam/newkey.html', RequestContext(request,locals()))
    elif request.method =='POST':
        form = NewRecordForm(request.POST)
        if form.is_valid():
            obj,created=AwsAccounts.objects.get_or_create(
                account_id = form.cleaned_data['account_id'],
                access_key_id = form.cleaned_data['access_key_id'],
                access_key = form.cleaned_data['access_key']
            )
            if created:
                message="Success!"
            else:
                message="Record exists!"

            data = AwsAccounts.objects.all()
            return ShowKey(request,message)
        else:
            return render_to_response('iam/newkey.html', RequestContext(request,locals()))

def  ShowKey(request,message):
    data = AwsAccounts.objects.all()
    results = []
    for i in data:
        if len(i.access_key) > 8:
            i.access_key = "".join([ '*' for x in range(len(i.access_key)-8)]) + i.access_key[-8:]
            results.append({'account_id':i.account_id,'access_key_id':i.access_key_id,'access_key':i.access_key})
    return render_to_response('iam/showkeys.html', RequestContext(request,{'results':results,'message':message}))