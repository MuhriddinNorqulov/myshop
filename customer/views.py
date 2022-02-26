from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from cart.cart import Cart
from product.models import Product
from wishlist.wishlist_cart import Wishlist
from store.usescart import dataCart


def logout_user(request):
    cart = Cart(request)
    wishlist_cart = Wishlist(request)

    if request.user.is_authenticated:
        logout(request)

        new_cart = Cart(request)
        for id, quantity in cart.iter_for_order().items():
            product = Product.objects.get(id=id)
            new_cart.add(product, int(quantity))

        new_wishlist_cart = Wishlist(request)
        product_ids = wishlist_cart.wishlist
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            new_wishlist_cart.add_wishlist(product)

    return redirect('store:store')


def user_login(request):
    usercart = dataCart(request)
    form = LoginForm()
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    for item in Cart(request).iter_for_order():
                        print(item)
                    return redirect('store:store')
                else:
                    print('Disabled account')
            else:
                print('Invalid login')

    context = {
        'form': form,
        'usercart': usercart,
    }
    return render(request, 'account/login_page.html', context)


def register(request, url):
    usercart = dataCart(request)
    form = UserRegisterForm()
    if request.POST:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration completed successfully!')
            return redirect(url)
        else:
            error = str(form.errors).split('<li>')[2].split('<')[0]
            print(error)
            messages.error(request, error)

    context = {
        'form': form,
        'usercart': usercart
    }

    return render(request, 'account/registration.html', context)

