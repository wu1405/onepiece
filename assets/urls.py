from django.conf.urls import patterns, url
from assets import views

urlpatterns = patterns('assets.views',
                       url(r'addAwsAccount/$', 'addAwsAccount'),
                       url(r'listAwsAccounts/$', 'listAwsAccounts'),
                       url(r'loadAwsAssets/$', 'loadAwsAssets'),
                       url(r'fetchAll/$', 'fetchAll'),
                       url(r'^$', 'listInstance'),
                       url(r'findAssets/$', 'findAssets'),
                       url(r'^ec2InstanceList/$', views.EC2InstanceList.as_view()),
                       url(r'^ec2InstanceDetail/(?P<instance_id>[0-9a-z\-]+)/$', views.EC2InstancegDetail.as_view()),
                       )
