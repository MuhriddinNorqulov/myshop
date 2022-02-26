import json
from django.http import JsonResponse
from store.usescart import dataCart
from product.models import Product


def add(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    product = Product.objects.get(id=product_id)
    data_cart = dataCart(request)
    wishlist_cart = data_cart['wishlist']
    wishlist_cart.add_wishlist(product)

    return JsonResponse(f"{product} wishlistga qo'shildi", safe=False)


def remove(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    product = Product.objects.get(id=product_id)
    data_cart = dataCart(request)
    wishlist_cart = data_cart['wishlist']
    wishlist_cart.remove_wishlist(product)

    return JsonResponse(f"{product} wishlistdan o'chirildi", safe=False)