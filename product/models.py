import sys
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
import json
from mptt.models import TreeForeignKey, MPTTModel
from django.utils.text import slugify


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True, null=True)
    img = models.ImageField(upload_to='products')
    price = models.FloatField()
    quantity = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    slug = models.SlugField(blank=True, null=True)
    # url = models.URLField(blank=True, null=True)

    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (650, 650)
    MAX_SIZE = 3145728

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.price}")

        image = self.img
        img = Image.open(image)
        new_image = img.convert("RGB")

        max_width, max_height = self.MAX_RESOLUTION
        min_width, min_height = self.MIN_RESOLUTION

        if img.height > max_height:

            height = img.height / max_height
        else:
            height = 1

        resized_new_image = new_image.resize((int(img.width / height), int(img.height / height)), Image.ANTIALIAS)

        filestream = BytesIO()
        resized_new_image.save(filestream, 'jpeg', quality=98)
        filestream.seek(0)
        name = '{}.{}'.format(*self.img.name.split('.'))
        print('name: ', name)
        self.img = InMemoryUploadedFile(
            filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
        )

        super().save(*args, **kwargs)

    class Meta:
        ordering = ('name',)

    @property
    def stock(self):
        return True

    def __str__(self):
        return self.name

    @property
    def get_json_info(self):
        info = {
            'id': self.id,
            'category': self.category.name,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'img': self.img.url,
            'description': self.description,
            'available': self.available,
            'stock': self.stock,
        }

        return json.dumps(info)



