#!/usr/bin/env python
# -*- coding:UTF-8 -*-
"""


"""
from boto import ec2
from boto.exception import EC2ResponseError
import boto
import pymongo
from pymongo.read_preferences import ReadPreference
from django.db import models

from mongoengine import DynamicDocument, StringField, DateTimeField, ListField, connect, DictField, BooleanField

from sysadmin.base import get_env_variable


con = connect(get_env_variable("MONGODB_DATABASE"), host=get_env_variable("MONGO_HOST"),
              port=int(get_env_variable("MONGO_PORT")), username=get_env_variable("MONGO_USER"),
              password=get_env_variable("MONGO_PASS"),read_preference=ReadPreference.PRIMARY)

class AwsAccounts(models.Model):
    #aws账号ID 074470703156
    account_id=models.CharField(null=False,blank=False,db_column="account_id",db_index=True,unique=True,verbose_name="账号",max_length=50)
    #Acess key id
    access_key_id=models.CharField(null=False,blank=False,db_column="access_key_id",db_index=True,unique=True,verbose_name="ACCESS_KEY_ID",max_length=50)
    #Access key
    access_key=models.CharField(null=False,blank=False,db_column="access_key",db_index=True,unique=True,verbose_name="ACCESS_KEY",max_length=50)


class EC2Instance(DynamicDocument):
    instance_id = StringField(primary_key=True)
    account_id = StringField()
    instance_type = StringField()
    region = StringField()
    public_dns_name = StringField()
    private_dns_name = StringField()
    state = StringField()
    key_name = StringField()
    instance_type = StringField()
    launch_time = DateTimeField()
    image_id = StringField()
    placement = StringField()
    placement_group = StringField()
    placement_tenancy = StringField()
    kernel = StringField()
    ramdisk = StringField()
    architecture = StringField()
    hypervisor = StringField()
    virtualization_type = StringField()
    monitored = BooleanField()
    monitoring_state = StringField()
    spot_instance_request_id = StringField()
    subnet_id = StringField()
    vpc_id = StringField()
    private_ip_address = StringField()
    ip_address = StringField()
    platform = StringField()
    root_device_name = StringField()
    root_device_type = StringField()
    instance_name = StringField()
    block_devices = ListField()
    security_groups = ListField()
    interfaces = ListField()
    tags = DictField()
    ebs_optimized = BooleanField()

    meta = {"collection": "instances"}


class MongoTool:
    collection = None

    def __init__(self):
        self.collection = con[get_env_variable("MONGODB_DATABASE")].instances


    # 获取所有的数据记录
    def getInstances(self, page=None, perPage=None, queries=None, cols=None, sorts=None, offset=None):
        rs = {}
        data = []
        filters = {}
        if queries != None:
            filters = queries

        if sorts == None or len(sorts) == 0:
            sorts = [("launch_time", pymongo.DESCENDING)]

        cur = self.collection.find(filter=filters, projection=cols).sort(sorts).skip(offset).limit(perPage)
        for document in cur:
            data.append(document)
        rs['queryRecordCount'] = rs['totalRecordCount'] = self.collection.find(filter=filters).count()
        rs['records'] = data
        return rs

    # 获取所有的列名
    def getAllColumnNames(self):
        cur = self.collection.find()
        columns = {}
        for doc in cur:
            for key in doc:
                columns[key]="1"
        return columns.keys()

    # # 插入或者更新aws instance记录，如果已经存在则更新，如果没有则插入
    # def insertOrUpdateInstances(self, instances):
    #     results = {}
    #     results['error_count'] = 0
    #     results['modified_count'] = 0
    #     results['total_record'] = len(instances)
    #     for instance in instances:
    #         # try:
    #         rs = self.collection.instances.update_one(
    #             {'_id': instance['_id']},
    #             {'$set': instance},
    #             upsert=True
    #         )
    #         results['modified_count'] = results['modified_count'] + rs.modified_count
    #         # except:
    #         # results['error_count'] = results['error_count'] + 1
    #
    #     return results

    def findAssets(self, filters, projections):
        cur = self.collection.find(filter=filters, projection=projections)
        data = []
        for document in cur:
            data.append(document)
        return data


class AwsTool:
    # 获取某个AWS账号下所有region的所有Instance
    def loadAllInstance(self, aws_access_key_id, aws_secret_access_key):
        results = {}
        results['error_count'] = 0
        results['modified_count'] = 0
        results['total_record'] = 0
        for region in ec2.regions():
            try:
                conn = ec2.connect_to_region(region.name, aws_access_key_id=aws_access_key_id,
                                             aws_secret_access_key=aws_secret_access_key)
                accountid = boto.connect_iam(aws_access_key_id=aws_access_key_id,
                                             aws_secret_access_key=aws_secret_access_key).get_user().arn.split(':')[4]
                instances = conn.get_only_instances()
            except EC2ResponseError as e:
                print e

            for instance in instances:
                results['total_record'] = results['total_record'] + 1
                ins = EC2Instance()

                ins.instance_id = instance.id
                ins.account_id = accountid
                ins.instance_type = instance.instance_type
                ins.region = region.name
                ins.public_dns_name = instance.public_dns_name
                ins.private_dns_name = instance.private_dns_name
                ins.state = instance.state
                ins.key_name = instance.key_name
                ins.instance_type = instance.instance_type
                ins.launch_time = instance.launch_time
                ins.image_id = instance.image_id
                ins.placement = instance.placement
                ins.placement_group = instance.placement_group
                ins.placement_tenancy = instance.placement_tenancy
                ins.kernel = instance.kernel
                ins.ramdisk = instance.ramdisk
                ins.architecture = instance.architecture
                ins.hypervisor = instance.hypervisor
                ins.virtualization_type = instance.virtualization_type
                ins.monitored = instance.monitored
                ins.monitoring_state = instance.monitoring_state
                ins.spot_instance_request_id = instance.spot_instance_request_id
                ins.subnet_id = instance.subnet_id
                ins.vpc_id = instance.vpc_id
                ins.private_ip_address = instance.private_ip_address
                ins.ip_address = instance.ip_address
                ins.platform = instance.platform
                ins.root_device_name = instance.root_device_name
                ins.root_device_type = instance.root_device_type

                # get tags
                ins.tags = instance.tags
                if instance.tags.has_key("Name"):
                    ins.instance_name = instance.tags['Name']
                else:
                    ins.instance_name = None

                # ins['block_device_mapping']=instance.block_device_mapping # – The Block Device Mapping for the instance.
                block_devices = []

                for device in instance.block_device_mapping:
                    block_devices.append(device)
                ins.block_devices = block_devices

                security_groups = []
                for sgroup in instance.groups:
                    securityInfo = {}
                    securityInfo['id'] = sgroup.id
                    securityInfo['name'] = sgroup.name
                    security_groups.append(securityInfo)
                ins.security_groups = security_groups

                interfaces = []
                for interface in instance.interfaces:
                    ifs = {}
                    ifs['id'] = interface.id
                    ifs['subnet_id'] = interface.subnet_id
                    ifs['vpc_id'] = interface.vpc_id
                    ifs['availability_zone'] = interface.availability_zone
                    ifs['description'] = interface.description
                    ifs['owner_id'] = interface.owner_id
                    ifs['status'] = interface.status
                    ifs['mac_address'] = interface.mac_address
                    ifs['private_ip_address'] = interface.private_ip_address
                    interfaces.append(ifs)
                ins.interfaces = interfaces
                ins.ebs_optimized = instance.ebs_optimized
                try:
                    rs = ins.save()
                    results['modified_count'] = results['modified_count'] + 1
                except:
                    results['error_count'] = results['error_count'] + 1

        return results