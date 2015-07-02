__author__ = 'wuhongbin'
from django.db import models
# class Bill_Mobo(models.Model):
#         date = models.DateField()
#         total_today = models.IntegerField(max_length=10)
#         total_all = models.IntegerField(max_length=10)
#
#
# class Bill_Voga(models.Model):
#         date = models.DateField()
#         total_today = models.IntegerField(max_length=10)
#         total_all = models.IntegerField(max_length=10)
#
#
# class Bill_Cypay(models.Model):
#         date = models.DateField()
#         total_today = models.IntegerField(max_length=10)
#         total_all = models.IntegerField(max_length=10)
class Bill(models.Model):
    date = models.DateField()
    cost_oneday = models.IntegerField(max_length=10)
    cost_total = models.IntegerField(max_length=10)
    account_id = models.CharField(max_length=30)
    class Meta:
        unique_together =("date", "account_id")
