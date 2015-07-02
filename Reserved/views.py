#!/usr/bin/env python
# -*- coding:UTF-8 -*-
from django.shortcuts import render, render_to_response
from Reserved.models import Reserved_tmp, Reserved_final
# INFO is our asset tables. All instance details include
from boto.ec2.connection import EC2Connection
from boto.ec2 import get_region
from django.contrib.auth.decorators import login_required
import os
import logging
import pymongo
#from django.db.models import Count, Min, Sum, Avg
from pymongo.read_preferences import ReadPreference
from mongoengine import DynamicDocument, StringField, DateTimeField, ListField, connect, DictField, BooleanField
from sysadmin.base import get_env_variable
from assets.models import AwsAccounts

#uri = "mongodb://onepiece:onepiece123@127.0.0.1:27017/onepiece"
#client = pymongo.MongoClient(uri)
#db = client.onepiece


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %Y-%m-%d %H:%M:%S',
                    filename='info.log',
                    filemode='w')

@login_required
def GetRI(request, account_ids):
    Reserved_tmp.objects.all().delete()
    count_num = 0

    for account_id in account_ids.split('-'):
        logging.info("the current account_id is %s" % account_id)
        areas = ('ap-southeast-1', 'sa-east-1', 'eu-west-1')

        QuerysetList = []
        for area in areas:
            #awskey = os.environ.get('%s_readkey' % account)
            awskey = AwsAccounts.objects.get(account_id=account_id).access_key_id
            #awssecret = os.environ.get('%s_readsecret' % account)
            awssecret = AwsAccounts.objects.get(account_id=account_id).access_key
            myRegion = get_region(area)
            conn = EC2Connection(aws_access_key_id=awskey, aws_secret_access_key=awssecret, region=myRegion)

            result = conn.get_all_reserved_instances()
            #QuerysetList = []
            for i in result:
                if i.state == 'active':
                    QuerysetList.append(
                        Reserved_tmp(region=i.availability_zone, type=i.instance_type, count=i.instance_count,
                                     duration=i.duration, end=i.end, account_id=account_id))
                    count_num += 1
        Reserved_tmp.objects.bulk_create(QuerysetList)
    rs = "%s results insert into Reserved_tmp succeed" % count_num
    logging.info(rs)

    #monogo connection
    con = connect(get_env_variable("MONGODB_DATABASE"), host=get_env_variable("MONGO_HOST"),
                  port=int(get_env_variable("MONGO_PORT")), username=get_env_variable("MONGO_USER"),
                  password=get_env_variable("MONGO_PASS"),read_preference=ReadPreference.PRIMARY)
    collection = con[get_env_variable("MONGODB_DATABASE")].instances


    # ALL the type  Merge
    TypeList = []
    for i in Reserved_tmp.objects.values('type').annotate().order_by():
        TypeList.append(i['type'])
    #for i in Info.objects.values('type').annotate().order_by():
    for i in collection.distinct('instance_type'):
        #TypeList.append(i['type'])
        TypeList.append(i)
    TypeList = list(set(TypeList))
    logging.info("All type is %s" % TypeList)

    # All the region
    RegionList = []
    for i in Reserved_tmp.objects.values('region').annotate().order_by():
        RegionList.append(i['region'])
    logging.info("All type is %s" % RegionList)

    # insert into the table "Reserved_final"
    Reserved_final.objects.all().delete()
    result = []
    count_num2 = 0

    for account_id in account_ids.split('-'):

        logging.info("the current account_id is %s" % account_id)
        for i in RegionList:
            for j in TypeList:
                ri_num_tmp = lambda x, y: Reserved_tmp.objects.filter(region=x, type=y, account_id=account_id).extra(
                    select={'total': 'sum(count)'}).values()[0]['total'] if \
                    Reserved_tmp.objects.filter(region=x, type=y, account_id=account_id).extra(
                        select={'total': 'sum(count)'}).values()[0]['total'] else 0
                #used_num_tmp = Info.objects.filter(region=i, type=j, status='running', account=account).count()
                used_num_tmp = collection.find(filter={"instance_type":j,"placement":i,"state":"running","account_id":account_id}).count()
                result.append(Reserved_final(region=i,
                                             type=j,
                                             used_num=used_num_tmp,
                                             ri_num=ri_num_tmp(i, j),
                                             delta=int(ri_num_tmp(i, j) - used_num_tmp),
                                             account_id=account_id))
                count_num2 += 1
    Reserved_final.objects.bulk_create(result)
    rs2 = "%s results insert into Reserved_final succeed" % count_num2
    logging.info(rs2)

    return render_to_response('reserved/insert_ri.html', {'rs': rs, 'rs2': rs2})

@login_required
def ShowTable(request):
    results = []
    for i in Reserved_final.objects.all():
        results.append(
            {'region': i.region, 'type': i.type, 'used_num': i.used_num, 'ri_num': i.ri_num, 'delta': i.delta,
             'account_id': i.account_id})

    return render_to_response('reserved/show_table.html', {'results': results})

