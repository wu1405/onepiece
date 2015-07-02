#!/usr/bin/env python
#-*- coding:UTF-8 -*-
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from curd.models import Curd
from curd.forms import NewRecordForm

#/curd/list
@login_required
def List(request):
    page = request.GET.get('page')
    #DB查询相关API参考：https://docs.djangoproject.com/en/1.6/topics/db/queries/
    data = Curd.objects.all()
    return backToHomePage(request,data,'')

#/curd/create
@login_required
def Create(request):
    if request.method == 'GET':
        title="新建用户"
        form = NewRecordForm()
        return render_to_response('curd/newUser.html', RequestContext(request,locals()))
    elif request.method =='POST':
        form=NewRecordForm(request.POST)
        if form.is_valid():
            obj,created=Curd.objects.get_or_create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                age=form.cleaned_data['age'],
                homePage=form.cleaned_data['homePage'],
                isMarried=form.cleaned_data['isMarried']
            )
            if created:
                message="Success!"
            else:
                message="Record exists!"

            data = Curd.objects.all()
            return backToHomePage(request,data,message)
        else:
            return render_to_response('curd/newUser.html', RequestContext(request,locals()))

def InfoToUpdate(request):
    if request.method == 'GET':
        user = request.GET.get('user')
        if user:
            title="更新用户"
            data = Curd.objects.get(name=user)
            form=NewRecordForm(initial = {
                'name':data.name,
                'email':data.email,
                'homePage':data.homePage,
                'age':data.age,
                'isMarried':data.isMarried
            })
            form.fields['name'].widget.attrs['readonly'] = True
            return render_to_response('curd/userInfo.html', RequestContext(request,locals()))
    elif request.method == 'POST':
        user = request.POST.get('name')
        data = Curd.objects.get(name = user)
        form=NewRecordForm(request.POST,instance=data)
        if form.is_valid():
            form.save()
            data = Curd.objects.all()
            return backToHomePage(request,data,'更新成功')
        else:
            return render_to_response('curd/userInfo.html', RequestContext(request,locals()))




def backToHomePage(request,data,message):
    paginator = Paginator(data, 10)
    page = request.GET.get('page')
    try:
        show_lines = paginator.page(page)
    except PageNotAnInteger:
        show_lines = paginator.page(1)
    except EmptyPage:
        show_lines = paginator.page(paginator.num_pages)
    return render_to_response('curd/list.html', RequestContext(request, {'lines': show_lines,'message':message}))


def Search(request):
    keyword = request.GET.get('keyword')
    if keyword:

        #模糊查询
        #参考API https://docs.djangoproject.com/en/1.6/ref/models/querysets/#std:fieldlookup-contains
        # data = Curd.objects.filter(name__contains = keyword)

        #查询名字或者邮箱字段包含查询字符的结果集
        #参考：https://docs.djangoproject.com/en/1.6/topics/db/queries/#complex-lookups-with-q-objects
        data = Curd.objects.filter(Q(name__contains=keyword) | Q(email__contains=keyword))
        return backToHomePage(request,data,'')




def Delete(request):
    if request.method == 'GET':
        user = request.GET.get('user')
        if user:
            data = Curd.objects.get(name=user)
            data.delete()
            return backToHomePage(request,Curd.objects.all(),'删除成功')



