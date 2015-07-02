from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('login.views',
    # Examples:
    # url(r'^$', 'sysadmin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^curd/', include('curd.urls')),
    url(r'^toplogy/', include('toplogy.urls')),
    url(r'^assets/', include('assets.urls')),
    url(r'reserved/',include('Reserved.urls')),
    url(r'billing/',include('Billing.urls')),
    url(r'iam/',include('iam.urls')),
    url(r'^$', 'Index'),
    url(r'^index/$', 'Index'),
    url(r'^login/$', 'Login'),
    url(r'^logout/$', 'Logout'),
)

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT )
