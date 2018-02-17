from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    short_description = models.TextField(blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    rating = models.CharField(max_length=6, default='0', choices=(
        ('0', 0),
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
    ))
    sum_rating = models.FloatField(default=0)
    average_rating = models.FloatField(default=0)
    nmb_of_rating = models.PositiveIntegerField(default=0)
    add_date = models.DateTimeField(auto_now_add=True)

    def rating_change(self):
        self.sum_rating += int(self.rating)
        self.nmb_of_rating += 1
        return self.save()

    def save(self, *args, **kwargs):
        try:
            self.average_rating = self.sum_rating/self.nmb_of_rating
        except ZeroDivisionError:
            pass
        super(Product, self).save(*args, **kwargs)

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
