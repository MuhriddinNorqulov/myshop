from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product, Category
from .models import Slider
from .usescart import dataCart
from discount.forms import CouponApplyForm
from order.forms import ShippingCreatForm
from customer.forms import LoginForm
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def checkout(request):
    usercart = dataCart(request)
    cart = usercart['cart']
    login_form = LoginForm()
    shipping_form = ShippingCreatForm()
    if request.user.is_authenticated:
        customer_check = True
    else:
        customer_check = False
    if request.POST:
        customer_option = request.POST.get('customer')
        if customer_option == 'new-user':
            return redirect('account:register', url='store:checkout')
        elif customer_option == 'guest':
            customer_check = True

    context = {
        'customer_check': customer_check,
        'login_form': login_form,
        'shipping_form': shipping_form,
        'usercart': usercart,
        'cart': cart,
    }
    return render(request, 'store/checkout.html', context)


def wishlist(request):
    usercart = dataCart(request)
    wishlist = usercart['wishlist']

    context = {
        'wishlist': wishlist,
        'usercart': usercart
    }
    return render(request, 'wishlist/wishlist_cart.html', context)


def shopping_cart(request):
    data_cart = dataCart(request)
    cart = data_cart['cart']
    coupon_form = CouponApplyForm()

    context = {
        'coupon_form': coupon_form,
        'cart': cart,
        'usercart': data_cart
    }

    return render(request, 'store/cart.html', context)


def index(request):

    slider = Slider.objects.all()
    products = Product.objects.all()

    usercart = dataCart(request)

    data = {
        'slider': slider,
        'products': products,
        'usercart': usercart
    }
    return render(request, 'store/index.html', data)


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    data = {
        'usercart': dataCart(request),
        'product': product
    }
    return render(request, 'store/product_detail.html', data)


@require_GET
def product_search(request):
    text = request.GET.get('product-search')
    object_list = Product.objects.filter(name__icontains=text)
    paginator = Paginator(object_list, 3)  # По 3 статьи на каждой странице.
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        # 'result': object_list,
        'posts': posts,
        'page': page
    }
    return render(request, 'store/search.html', context)