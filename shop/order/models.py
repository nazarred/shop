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
    products = models.ManyToManyField(ProductInCart)
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICE, default='Новий')
    add_date = models.DateTimeField(auto_now_add=True)

   # попробувати зробити при допомозі агрегації
    def get_total_price(self):
        return sum(product.get_total_product_price for product in self.products.all())

    def __str__(self):
        user = self.user if self.user else 'Not register'
        return '%s (%s %s)' % (user, self.first_name, self.last_name)

from .signals import delete_products_from_cart
