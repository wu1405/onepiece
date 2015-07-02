#!/usr/bin/env python
#-*- coding:UTF-8 -*-
from datetime import datetime
from django.core.validators import EmailValidator,URLValidator,MinValueValidator,MaxValueValidator
from django.db import models

class Curd(models.Model):
    #关于fields的用法参考https://docs.djangoproject.com/en/1.6/ref/models/fields/
    name=models.CharField(null=False,blank=False,db_column="name",db_index=True,unique=True,verbose_name="用户名",max_length=50)
    #关于validators的用法参考https://docs.djangoproject.com/en/1.6/ref/validators/
    email=models.CharField(blank=False,db_column="email",unique=True,verbose_name="邮箱",validators=[EmailValidator()],max_length=50)
    createDate=models.DateTimeField(verbose_name="创建时间",db_column="cdate",help_text="创建时间",auto_now_add=True)
    lastModify=models.DateTimeField(verbose_name="最后修改时间",db_column="ldate",help_text="最后修改时间",auto_now=True)
    isMarried=models.BooleanField(verbose_name="婚否",db_column="isMarried")
    homePage=models.URLField(verbose_name="个人主页",db_column="homePage",blank=True,validators=[URLValidator()])
    age=models.IntegerField(verbose_name="年龄",db_column="age",blank=False,validators=[MinValueValidator(1),MaxValueValidator(150)])
    class Meta:#更多Meta定义参考https://docs.djangoproject.com/en/1.6/ref/models/options/
        db_table="curd"#定义表名
        ordering=['-createDate']#按照创建时间排序
        get_latest_by="lastModify"#按照最近修改时间返回第一个记录

