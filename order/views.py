from django.shortcuts import render, redirect
from django.utils import timezone
from customer.forms import LoginForm
from django.contrib.auth import login, authenticate
from .models import Order, OrderItem
from django.contrib import messages
from cart.cart import Cart
from product.models import Product
from django.views.decorators.http import require_POST
from .forms import ShippingCreatForm
from django.http import HttpResponse
from store.usescart import dataCart


@require_POST
def shipping_check(request):
    usercart = dataCart(request)
    cart = usercart['cart']
    if len(cart) == 0:
        return redirect('store:shopping-cart')
    form = ShippingCreatForm(request.POST)
    if form.is_valid():
        shipping_address = form.save()
        if request.user.is_authenticated:
            order = cart
        else:
            order = anonymous_order(request)
        order.shipping_address = shipping_address
        order.ordered = True
        order.save()
        if not request.user.is_authenticated:
            cart = Cart(request)
            cart.clear()
        return redirect('store:store')
    else:
        return HttpResponse("Xatolik yuz berdi!")


def anonymous_order(request):
    cart = Cart(request)
    order = Order.objects.create()

    update_order(request, order)

    if cart.coupon:
        order.coupon = cart.coupon
    order.save()

    return order


def update_order(request, order, extend=True):
    cart = Cart(request)

    if not extend:
        for item in order:
            order.remove(item.product)

    for pk, quantity in cart.iter_for_order().items():
        try:
            product = Product.objects.get(id=pk)
            order_item, created_item = OrderItem.objects.get_or_create(order=order, product=product)
            if created_item:
                order_item.quantity = quantity
                order_item.date_add = timezone.now()
                order_item.save()
        except Product.DoesNotExist:
            pass


@require_POST
def check_user(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        username = cd['username']
        password = cd['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                order = Order.objects.get_or_create(customer=request.user, ordered=False)
                update_order(request, order, extend=False)
    else:
        error = str(form.errors).split('<li>')[2].split('<')[0]
        messages.error(request, error)

    return redirect('store:checkout')
