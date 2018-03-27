from django.contrib.sessions.models import Session
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, F, FloatField

from product.models import Product, ProductInCart


ORDER_STATUS_CHOICE = (
    ('Новий', 'Новий'),
    ('Обробка', 'Обробка'),
    ('Виконано', 'Виконано'),
    ('Скасовано', 'Скасовано'),
)


class Order(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    phone_nmb = models.CharField(max_length=15)
    address = models.TextField()
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICE, default='Новий')
    add_date = models.DateTimeField(auto_now_add=True)
    total_order_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_order_price = self.productinorder_set.aggregate(Sum('total_price'))['total_price__sum']
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        user = self.user if self.user else 'Not register'
        return '%s (%s %s)' % (user, self.first_name, self.last_name)


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    pcs = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    add_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        total_price = self.product.price*self.pcs
        if self.total_price != total_price:
            self.total_price = total_price
        super(ProductInOrder, self).save(*args, **kwargs)


from .signals import order_save
