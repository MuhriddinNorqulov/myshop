from .models import Order
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def admin_order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})