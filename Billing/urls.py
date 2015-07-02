from django.conf.urls import patterns, include, url

urlpatterns = patterns('Billing.views',
    url(r'^insert/ids=(.*)/delta=(\d{1,2})$', 'Update_Bill'),
    url(r'^showbill/$', 'Show_Bill'),
)
