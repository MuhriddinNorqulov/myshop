from product.models import Product
from django.conf import settings
from discount.models import Coupon
from order.models import Order


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')
        self.order_id = self.session.get('order_id')

    @property
    def order(self):
        if self.order_id:
            try:
                return Order.objects.get(id=self.order_id)
            except Order.DoesNotExist:
                return None
        return None

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        if self.coupon:
            total = (self.coupon.discount_percent/100)*self.get_total_price()
            return total
        return 0

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()

    def get_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values())

    def get_total_count(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def add(self, product, quantity=1, update=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': product.price}

        if update:

            self.cart[product_id]['quantity'] = quantity
        else:

            self.cart[product_id]['quantity'] += quantity

        self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __len__(self):
        total = sum([item['quantity'] for item in self.cart.values()])
        return total

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def iter_for_order(self):
        new_cart = {}
        product_ids = self.cart.keys()
        cart = self.cart.copy()
        for product in product_ids:
            new_cart[int(product)] = cart[str(product)]['quantity']
        return new_cart




