from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.safestring import mark_safe


def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(reverse('order:admin_order_detail', args=[obj.id])))


@admin.register(ShippingInfo)
class ShippingInfo_Admin(admin.ModelAdmin):
    list_display = ['phone_number', 'address', 'zipcode']


class OrderItem_Inline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItem_Inline]
    list_display = ['id', order_detail]

