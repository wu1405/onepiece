#!/usr/bin/env python
#-*- coding:UTF-8 -*-
import random
import string

#generate random string#
def randomstr(len, num_flag=True, low_flag=True, up_flag=False, special_flag=False):
    num = "0123456789"
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    special = "~!@#$%^&*()[]{}_=+-"
    str = ''
    if num_flag: str += num 
    if low_flag: str += lower
    if up_flag: str += upper
    if special_flag: str += special
    if str == '': str = num + lower
    return string.join(random.sample(str, len)).replace(" ", "") 

def IsAdmin(department):
    allow_list = (u'系统部-运维开发组', u'系统部-SA组')
    allow_flag = False
    for i in allow_list:
        if i in department:
            allow_flag = True
    return allow_flag

def FabRun(cmd):
    with settings(warn_only=True):
        out = run(cmd)
        return out

