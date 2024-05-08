from django.contrib import admin
from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter

from accounts.models import User,Otp,OtpChecked,Address
# from django_jalali.admin.filters import JDateFieldListFilter
# import django_jalali.admin as jadmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number','first_name','last_name','is_admin')
    list_filter = ('is_admin',)

@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ('phone_number','Random_code','created')


@admin.register(OtpChecked)
class OAdmin(admin.ModelAdmin):
    list_display = ('phone_number','Otp_code','created','block')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('formatted_address','state','county','village')




