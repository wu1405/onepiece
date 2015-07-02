__author__ = 'wuhongbin'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('iam.views',
    #url(r'^$', 'ShowKey'),
    url(r'^show/(.*)$', 'ShowKey'),
    url(r'^create/$', 'CreateKey'),
    url(r'^delete/$', 'DeleteKey'),
)
