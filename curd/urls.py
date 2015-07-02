from django.conf.urls import patterns, include, url

urlpatterns = patterns('curd.views',
    url(r'^$', 'List'),
    url(r'^list/$', 'List'),
    url(r'^create/$', 'Create'),
    url(r'^delete/$', 'Delete'),
    url(r'^search/$', 'Search'),
    url(r'^infoToUpdate/$', 'InfoToUpdate'),

)
