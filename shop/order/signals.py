from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Order


@receiver(post_save, sender=Order)
def delete_products_from_cart(sender, instance, **kwargs):
    instance.products.all().update(in_order=True)
    print(instance.products.all())

