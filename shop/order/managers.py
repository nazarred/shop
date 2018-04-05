from django.db import models
from product.models import ProductInCart


class ProductInOrderQuerySet(models.QuerySet):
    def create_from_cart(self, request, order):
        products_in_cart = ProductInCart.objects.user_cart(request, is_active=True).select_related('product')
        self.model.objects.bulk_create([
            self.model(
                order=order,
                product=product_in_cart.product,
                pcs=product_in_cart.pcs,
                total_price=product_in_cart.get_total_product_price)
            for product_in_cart in products_in_cart
        ])
        order.calculate_total_price()
