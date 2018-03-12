from django.db import models
from .utils import get_session_instance


class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super(ActiveProductManager, self).get_queryset().filter(is_active=True)


class CartManager(models.Manager):
    pass


class CartQuerySet(models.QuerySet):
    def user_cart(self, request):
        if request.user.is_authenticated:
            qs = self.filter(user=request.user)
        else:
            session = get_session_instance(request)
            qs = self.filter(session=session)
        return qs
