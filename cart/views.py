from django.shortcuts import get_object_or_404
from product.models import Product
from django.http import JsonResponse
import json
from store.usescart import dataCart


def add(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    count = data['count']
    update = data['isupdate']

    product = get_object_or_404(Product, id=product_id)
    data_cart = dataCart(request)
    cart = data_cart['cart']

    cart.add(product=product, quantity=int(count), update=bool(update))

    cart_info = {
        'quantity': len(cart),
        'total-price': cart.get_total_price(),
        "item-price": product.price * int(count)
    }
    cart_info = json.dumps(cart_info)

    return JsonResponse(f"{cart_info}", safe=False)


def remove(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    product = get_object_or_404(Product, id=product_id)
    data_cart = dataCart(request)

    cart = data_cart['cart']
    cart.remove(product)
    return JsonResponse(f"item={product} delete", safe=False)
