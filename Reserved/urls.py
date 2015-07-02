from django.conf.urls import patterns, include, url

urlpatterns = patterns('Reserved.views',
	url(r'^ri/account_ids=(.*)/$', 'GetRI'),
	url(r'^ri/showtable/$', 'ShowTable'),
    url(r'^$','ShowTable'),
)
