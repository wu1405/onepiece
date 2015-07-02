#!/usr/bin/env python
#-*- coding:UTF-8 -*-
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from login.forms import LoginForm
import re

def Login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render_to_response('login/login.html', RequestContext(request, {'form': form,}))
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                username = request.user.first_name
                Next = re.search(r"=/(.+)/", request.get_full_path())   #request.get_full_path() : like nginx's $request_uri . url like /login/?next=/index/
                if Next:
                    Next = Next.group(1)
                else:
                    Next = "index/"
                return HttpResponseRedirect("/%s" % Next)
            else:
                return render_to_response('login/login.html', RequestContext(request, {'form': form,'password_is_wrong':True}))
        else:
            return render_to_response('login/login.html', RequestContext(request, {'form': form,}))

@login_required
def Index(request):
    return HttpResponseRedirect('/toplogy/')

@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
