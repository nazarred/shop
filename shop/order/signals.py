from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import ProductInOrder, Order


@receiver(post_save, sender=ProductInOrder)
def order_save(sender, instance, **kwargs):
    instance.order.save()


