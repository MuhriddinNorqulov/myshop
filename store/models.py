from django.db import models
from product.models import Product

class Slider(models.Model):
    img = models.ImageField(upload_to='slider')
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=500)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product.name)
