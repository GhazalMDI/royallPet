from django.contrib import admin
import django_jalali.admin as jadmin
from django_jalali.admin.filters import JDateFieldListFilter

from order.models import Order,OrderItem,Coupon

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 2
@admin.register(Order)
class Admin(admin.ModelAdmin):
    list_display = ('user','f_name','l_name','postal_code','paid','created')
    inlines = [OrderItemInline]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code','discount','active','from_date','to_date')
    list_editable = ('active',)
    list_filter = (
        ('from_date',JDateFieldListFilter),
        ('to_date',JDateFieldListFilter)
    )





