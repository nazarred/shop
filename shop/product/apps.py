from django.apps import AppConfig


class ProductConfig(AppConfig):
    name = 'product'

    # такий спосіб зареєструвати сигнали чомусь не працює
    # def ready(self):
    #         import product.signals
