#!/usr/bin/env python
# -*- coding:UTF-8 -*-
from assets.models import EC2Instance

__author__ = 'SongJiao'
from rest_framework_mongoengine.serializers import DocumentSerializer

class EC2InstanceSerializer(DocumentSerializer):
    class Meta:
        model = EC2Instance
