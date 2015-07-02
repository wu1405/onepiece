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
def Test(request):
     return render_to_response('toplogy.html', RequestContext(request,locals()))


