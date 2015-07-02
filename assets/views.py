#!/usr/bin/env python
# -*- coding:UTF-8 -*-
import json
import boto
from bson import json_util
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
import pymongo
from rest_framework_mongoengine.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from assets.models import AwsTool, MongoTool, AwsAccounts
from assets.forms import AwsAccountsForm
from assets.models import EC2Instance
from assets.serializers import EC2InstanceSerializer


default_cols = ['instance_name', '_id', 'instance_type', 'placement', 'state', 'private_ip_address', 'ip_address',
                'key_name', 'launch_time', 'vpc_id', 'account_id']
# 根据用户输入的aws key来导入aws账号下所有的Instance资产信息
@login_required
def loadAwsAssets(request):
    if request.method == "GET":
        account_id=request.GET.get("id")
        awsAccount=AwsAccounts.objects.get(account_id=account_id)
        aws_access_key_id = awsAccount.access_key_id
        aws_secret_access_key = awsAccount.access_key
        results = AwsTool().loadAllInstance(aws_access_key_id, aws_secret_access_key)
        return render_to_response('assets/loadAwsAssetsResult.html', RequestContext(request, locals()))

@login_required
def addAwsAccount(request):
    if request.method =="POST":
        form=AwsAccountsForm(request.POST)
        if form.is_valid():
            aws_access_key_id = request.POST.get('aws_access_key_id', '')
            aws_secret_access_key = request.POST.get('aws_secret_access_key', '')
            account_id = boto.connect_iam(aws_access_key_id=aws_access_key_id,
                                             aws_secret_access_key=aws_secret_access_key).get_user().arn.split(':')[4]
            AwsAccounts.objects.get_or_create(account_id=account_id,access_key_id=aws_access_key_id,access_key=aws_secret_access_key)
            message="success"
            data = AwsAccounts.objects.all()
            form = AwsAccountsForm()
            return render_to_response('assets/awsAccounts.html', RequestContext(request, locals()))
        else:
            message="error"
            data = AwsAccounts.objects.all()
            form = AwsAccountsForm()
            return render_to_response('assets/awsAccounts.html', RequestContext(request, locals()))


@login_required
def listAwsAccounts(request):
    data = AwsAccounts.objects.all()
    form = AwsAccountsForm()
    return render_to_response('assets/awsAccounts.html', RequestContext(request, locals()))

@login_required
def listInstance(request):
    if request.GET.keys():
        cols = request.GET.keys()
    else:
        cols = default_cols
    request.session['cols'] = cols
    # 获取所有的列名
    mongoTool = MongoTool()
    allColumns = mongoTool.getAllColumnNames()
    return render_to_response('assets/list.html', RequestContext(request, locals()))


# 根据MONGODB FIND 语法查找信息
# @login_required
def findAssets(request):
    if request.method == "POST":
        filters = {}
        if request.POST.get("filters"):
            filters = eval(request.POST.get("filters"))

        projections = None
        if request.POST.get("projections"):
            projections = eval(request.POST.get("projections"))
        mongoTool = MongoTool()
        data = mongoTool.findAssets(filters=filters, projections=projections)
        return HttpResponse(content=json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))

    elif request.method == "GET":
        filters = {}
        if request.GET.get("filters"):
            filters = eval(request.GET.get("filters").encode("utf-8"))

        projections = None
        if request.GET.get("projections"):
            projections = eval(request.GET.get("projections").encode("utf-8"))
        mongoTool = MongoTool()
        data = mongoTool.findAssets(filters=filters, projections=projections)
        return HttpResponse(content=json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))


        # 负责为dynatable提供数据的ajax接口


@login_required
def fetchAll(request):
    if request.session.has_key('cols'):
        cols = request.session['cols']
    else:
        cols = default_cols
    # 获取当前页码
    page = 1
    if request.GET.get("page"):
        try:
            page = int(request.GET.get("page"))
        except (TypeError, ValueError):
            page = 1

            # 获取每页显示的记录条数
    perPage = 10
    if request.GET.get("perPage"):
        try:
            perPage = int(request.GET.get("perPage"))
        except (TypeError, ValueError):
            perPage = 10

    offset = 0
    if request.GET.get("offset"):
        try:
            offset = int(request.GET.get("offset"))
        except (TypeError, ValueError):
            offset = 0

    # 获取排序条件
    # fetchAll/?sorts[name]=1&page=1&perPage=10&offset=0
    sort = []
    for k in request.GET.keys():
        if k.startswith("sorts["):
            if request.GET.get(k) == "1":
                sort.append((k[6:-1], pymongo.ASCENDING))
            else:
                sort.append((k[6:-1], pymongo.DESCENDING))


    # 获取查询字符串
    queries = None
    for k in request.GET.keys():
        if k.startswith("queries["):
            keyword = request.GET.get(k)
            # 拼mongo 查询条件语句,自动检索所有的字段
            queries = {}
            tmp = []
            for col in cols:
                tmp.append({col: {'$regex': keyword, '$options': 'i'}})
            queries['$or'] = tmp
    mongoTool = MongoTool()
    data = mongoTool.getInstances(page=page, perPage=perPage, queries=queries, cols=cols, sorts=sort,
                                  offset=offset)
    return HttpResponse(content=json.dumps(data, default=json_serial))


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    if isinstance(obj, list):
        return ",".join(obj)
    if isinstance((obj, dict)):
        return str(obj)
    raise TypeError("Type not serializable")


class EC2InstanceList(ListCreateAPIView):
    queryset = EC2Instance.objects.all()
    serializer_class = EC2InstanceSerializer


class EC2InstancegDetail(RetrieveUpdateDestroyAPIView):
    lookup_field = "instance_id"
    queryset = EC2Instance.objects.all()
    serializer_class = EC2InstanceSerializer
