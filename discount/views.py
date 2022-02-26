from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from order.models import Order
from .forms import CouponApplyForm


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code=code, valid_from__lte=now,
                                        valid_to__gte=now, active=True)
            if request.user.is_authenticated:
                try:
                    order = Order.objects.get(customer=request.user, ordered=False)
                    order.coupon = coupon
                    order.save()
                except Order.DoesNotExist:
                    pass
            else:
                request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None

    return redirect('store:shopping-cart')

