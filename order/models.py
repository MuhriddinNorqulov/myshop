from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from discount.models import Coupon


class ShippingInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='Customer name')
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    zipcode = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address}:{self.zipcode}"


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    shipping_address = models.ForeignKey(ShippingInfo, on_delete=models.SET_NULL, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon, blank=True, null=True, on_delete=models.SET_NULL)

    def __iter__(self):
        for item in self.orderitem_set.all():
            yield item

    # def save(self, *args, **kwargs):
    #     if self.coupon:
    #         self.discount_percent = self.coupon.discount_percent
    #     super().save(*args, *kwargs)

    def add(self, product, quantity, update):
        order_item, created = OrderItem.objects.get_or_create(order=self, product=product)
        if update:
            order_item.quantity = quantity
        else:
            order_item.quantity += quantity
        order_item.save()

    def remove(self, product):
        try:
            order_item = OrderItem.objects.get(order=self, product=product)
            order_item.delete(using=None, keep_parents=False)
            self.save()

        except:
            print('dfasd')

    def get_discount(self):
        if self.coupon:
            total = self.get_total_price() * self.coupon.discount_percent / 100
            return total
        return 0

    def get_total_price_after_discount(self):
        if self.coupon:
            return self.get_total_price() * (1 - self.coupon.discount_percent / 100)
        return self.get_total_price()

    def get_total_price(self):
        return sum([item.total_price() for item in self.orderitem_set.all()])

    def get_total_count(self):
        return sum([item.quantity for item in self.orderitem_set.all()])

    def __len__(self):
        return self.get_total_count()

    def __str__(self):
        return f"{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date_add = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product} item {self.quantity}"

    def total_price(self):
        return self.quantity * self.product.price
