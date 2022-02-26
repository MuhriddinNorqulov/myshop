from django.urls import path
from .views import check_user, shipping_check
from .admin_panel import admin_order_detail
app_name = 'order'

urlpatterns = [
    path('admin/order/<order_id>', admin_order_detail, name='admin_order_detail'),
    path('check/user', check_user, name='check-user'),
    path('shipping/check/', shipping_check, name='shipping-check')
]