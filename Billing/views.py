#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from Billing.models import Bill
import boto.ec2.cloudwatch
import logging
import boto.ec2
from boto.ec2 import get_region
import datetime
from datetime import timedelta
from assets.models import AwsAccounts


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %Y-%m-%d %H:%M:%S',
                    filename='billing.log',
                    filemode='w')


def Update_Bill(request, ids, delta):
#   id = "958972517121-378009643266-154785747698"
#   "/billing/insert/ids=958972517121-378009643266-154785747698/delta=0"
    billingkey = AwsAccounts.objects.get(account_id='074470703156').access_key_id
    billingsecret = AwsAccounts.objects.get(account_id='074470703156').access_key
    conn = boto.ec2.cloudwatch.connect_to_region('us-east-1', aws_access_key_id=billingkey, aws_secret_access_key=billingsecret)
    Metrics = conn.list_metrics(metric_name=u'EstimatedCharges', namespace=u'AWS/Billing')
    #end = datetime.datetime(2015,6,15)
#   begin = datetime.datetime(2015,3,20)
    end = datetime.date.today()+timedelta(days=-int(delta))
    begin = end + timedelta(days=-1)
    daybeforebegin = begin + timedelta(days=-1)
    message = []
    for id in ids.split('-'):
        for metric in Metrics:
            if  [id]  in metric.dimensions.values() and u'ServiceName' not in metric.dimensions:
                total = metric.query(begin, end, 'Average', period=86400)[0][u'Average']
                total_early = metric.query(daybeforebegin, begin, 'Average', period=86400)[0][u'Average']
                if str(begin).split('-')[1] == str(daybeforebegin).split('-')[1]:
                    oneday = total - total_early
                else:
                    oneday = total

                try:
                    logging.info("yesterday is %s, one day charge is %s" % (total, oneday))
                    f = Bill(account_id=id, date=begin, cost_total=total, cost_oneday=oneday )
                    f.save()
                    message.append("date:%s,id:%s, insert ok" % (begin, id))
                except Exception as e:
                    message.append(e)

    return render_to_response('billing/insert.html', {'result': message})

def Show_Bill(request):
    ids = ["958972517121", "378009643266", "154785747698"]
    date_result = []
    total_all_voga = []
    total_today_voga = []
    total_all_mobo = []
    total_today_mobo = []
    total_all_cypay = []
    total_today_cypay = []
    result=request.POST.get('reservation', '')

    for id in ids:
        # default chart
        if not result:
            if Bill.objects.filter(account_id="958972517121").order_by("date"):
                start=str(Bill.objects.filter(account_id="958972517121").order_by("date")[0].date)
                end=str(Bill.objects.filter(account_id="958972517121").order_by("-date")[0].date)
                #voga
                if id == "958972517121":
                    objs = Bill.objects.filter(account_id=id ).order_by("date")
                    for obj in objs:
                        date_result.append(str(obj.date))
                        total_all_voga.append(int(obj.cost_total))
                        total_today_voga.append(int(obj.cost_oneday))
                #mobo
                if id == "378009643266":
                    objs = Bill.objects.filter(account_id=id).order_by("date")
                    for obj in objs:
                        total_all_mobo.append(int(obj.cost_total))
                        total_today_mobo.append(int(obj.cost_oneday))
                #cypay
                if id == "154785747698":
                    objs = Bill.objects.filter(account_id=id ).order_by("date")
                    for obj in objs:
                        total_all_cypay.append(int(obj.cost_total))
                        total_today_cypay.append(int(obj.cost_oneday))
            else:
                message = "No data found"
                return render_to_response('billing/insert.html', {'result': message})

        # custom chart
        else:
            start=result.split(" - ")[0]
            end=result.split(" - ")[1]
            if id == "958972517121":
                objs = Bill.objects.order_by("date").filter(account_id=id, date__range=(start, end))
                for obj in objs:
                    date_result.append(str(obj.date))
                    total_all_voga.append(int(obj.cost_total))
                    total_today_voga.append(int(obj.cost_oneday))
            #mobo
            if id == "378009643266":
                objs = Bill.objects.order_by("date").filter(account_id=id, date__range=(start, end))
                for obj in objs:
                    total_all_mobo.append(int(obj.cost_total))
                    total_today_mobo.append(int(obj.cost_oneday))
            #cypay
            if id == "154785747698":
                objs = Bill.objects.order_by("date").filter(account_id=id, date__range=(start, end))
                for obj in objs:
                    total_all_cypay.append(int(obj.cost_total))
                    total_today_cypay.append(int(obj.cost_oneday))

    return render_to_response('billing/billing.html', RequestContext(request, locals()))

