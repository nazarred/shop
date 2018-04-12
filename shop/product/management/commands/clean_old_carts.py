from django.core.management.base import BaseCommand
from importlib import import_module
from product.models import ProductInCart

from django.conf import settings

SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


class Command(BaseCommand):
    help = 'Видаляє продукти в корзині у яких закінчився термін дії сесії' \
           '(за умови,що сесії зберігаються в кеші і автоматично видаляються після закінчення терміну дії)'

    def handle(self, *args, **options):
        nmb = 0
        for product in ProductInCart.objects.filter(user=None):
            session_key = product.session
            if not SessionStore().exists(session_key):
                product.delete()
                nmb += 1
        self.stdout.write(self.style.SUCCESS('Successfully deleted "%s" products in carts' % nmb))
