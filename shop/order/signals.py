from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProductInOrder


@receiver(post_save, sender=ProductInOrder)
def order_save(sender, instance, **kwargs):
    instance.order.calculate_total_price()
