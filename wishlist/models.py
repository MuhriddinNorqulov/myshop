from django.db import models
from django.conf import settings
from product.models import Product


class Wishlist(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True, null=True)

    def add_wishlist(self, product):
        if product not in self.products.all():
            self.products.add(product)
        self.save()

    def remove_wishlist(self, product):
        if product in self.products.all():
            self.products.remove(product)

    def __len__(self):
        return len(self.products.all())

    def wishlist_iter(self):
        return self.products.all()

    def __iter__(self):
        for item in self.products.all():
            yield item

    def __str__(self):
        return f"{self.customer}-wishlist"
