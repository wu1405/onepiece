from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from sysadmin.models import *
from django import forms

#UserAdmin.list_display = ('username', 'email', 'first_name', 'department', 'mobile', 'location', 'is_staff', 'is_superuser', 'is_active')
#UserAdmin.search_fields = ('username', 'email', 'first_name', 'department', 'mobile')

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = MyUser


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            MyUser.objects.get(username=username)
        except MyUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('username', 'email', 'first_name', 'department', 'mobile', 'location', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'department', 'mobile')

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('mobile', 'department', 'job', 'location', 'company', 'sex', 'uac',)}),
    )

class IpListAdmin(admin.ModelAdmin):
    search_fields = ('ipaddr',)

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(IpList, IpListAdmin)
