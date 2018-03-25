from django.db import models
from .utils import get_session_instance


class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super(ActiveProductManager, self).get_queryset().filter(is_active=True)


class CartManager(models.Manager):
    pass


class CartQuerySet(models.QuerySet):
    def user_cart(self, request, in_order=False, is_active=None):
        if request.user.is_authenticated:
            qs = self.filter(user=request.user, in_order=in_order)
            if is_active is not None:
                qs = qs.filter(product__is_active=is_active)
        else:
            session = get_session_instance(request)
            qs = self.filter(session=session, in_order=in_order)
            if is_active is not None:
                qs = qs.filter(product__is_active=is_active)
        return qs
