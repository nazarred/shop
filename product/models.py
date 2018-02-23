from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class Product(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    short_description = models.TextField(blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    average_rating = models.FloatField(default=0)
    add_date = models.DateTimeField(auto_now_add=True)

    def get_nmb_of_rating(self):
        return self.productrating_set.all().count()

    def get_avg_rating_in_px(self):
        return 160*self.average_rating/5

    def get_main_image(self):
        return self.productimage_set.get(is_main=True)

    def get_not_main_images(self):
        return self.productimage_set.filter(is_main=False)

    def save(self, *args, **kwargs):
        self.average_rating = self.productrating_set.all().aggregate(Avg('rating'))['rating__avg']
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return "%s" % self.name


class ProductRating(models.Model):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    rating = models.CharField(max_length=6, default='0', choices=(
        ('0', 0),
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
    ))


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
