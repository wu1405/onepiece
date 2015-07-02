from django.contrib.auth.models import AbstractUser
from django.db import models

class MyUser(AbstractUser):
    #map to telephoneNumber
    mobile = models.CharField(max_length=30, blank=True, default='')
    #map to description
    department = models.CharField(max_length=255, blank=True, default='')
    #map to title
    job = models.CharField(max_length=100, blank=True, default='')
    #map to physicalDeliveryOfficeName
    location = models.CharField(max_length=30, blank=True, default='')
    #map to company
    company = models.CharField(max_length=100, blank=True, default='')
    #map to info
    sex = models.CharField(max_length=3, blank=True, default='')
    #map to userAccountControl
    uac = models.IntegerField(default=512)

    def __unicode__(self):
        return u'%s %s' % (self.username, self.first_name)
    

class IpList(models.Model):
    ipaddr = models.IPAddressField(unique=True)

    def __unicode__(self):
        return self.ipaddr

#admin.site.register(IpList, IpListAdmin)