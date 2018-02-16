from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    short_description = models.TextField(blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    rating = models.CharField(max_length=6, default='none', choices=(
        ('none', 0),
        ('one', 1),
        ('two', 2),
        ('three', 3),
        ('four', 4),
        ('five', 5),
    ))

    def __str__(self):
        return "%s" % self.name


class ProductComment(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    text = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True, default=None)
    image = models.ImageField(upload_to='static/products_images/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.product
