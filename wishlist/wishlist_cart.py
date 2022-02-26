from django.conf import settings
from product.models import Product


class Wishlist(object):
    def __init__(self, request):
        self.session = request.session

        wishlist = request.session.get(settings.WISHLIST_SESSION_ID)
        if not wishlist:
            wishlist = self.session[settings.WISHLIST_SESSION_ID] = [0]

        self.wishlist = wishlist

    def add_wishlist(self, product):
        if product.id not in self.wishlist:
            self.wishlist.append(product.id)
        self.save()

    def remove_wishlist(self, product):
        if product.id in self.wishlist:
            self.wishlist.remove(product.id)
        self.save()

    def __len__(self):
        cart = self.wishlist.copy()
        cart.remove(0)
        return len(cart)

    def __iter__(self):
        cart = self.wishlist.copy()
        cart.remove(0)
        product_ids = cart
        products = Product.objects.filter(id__in=product_ids)
        for item in products:
            yield item

    def save(self):
        self.session.modified = True
