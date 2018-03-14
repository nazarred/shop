from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ProductRating


@receiver(post_save, sender=ProductRating)
@receiver(post_delete, sender=ProductRating)
def save_product(sender, instance, **kwargs):
    product = instance.product
    product.save()

