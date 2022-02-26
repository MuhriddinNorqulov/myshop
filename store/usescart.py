from order.models import Order
from wishlist.models import Wishlist
from cart.cart import Cart
from wishlist.wishlist_cart import Wishlist as WishlistCart


def dataCart(request):
    if request.user.is_authenticated:
        user = request.user
        cart, created = Order.objects.get_or_create(customer=request.user, ordered=False)
        wishlist, created = Wishlist.objects.get_or_create(customer=request.user)

    else:
        user = None
        wishlist = WishlistCart(request)
        cart = Cart(request)

    data = {
        'user': user,
        'cart': cart,
        'wishlist': wishlist
    }

    return data