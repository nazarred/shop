from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.contrib.sessions.models import Session

from .managers import ActiveProductManager, CartManager, CartQuerySet

WIDTH_OF_RATING_STAR = 32  # ширина однієї зірочки рейтинга (static/images/stars.png)


class Product(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    short_description = models.TextField(blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    average_rating = models.FloatField(default=0, null=True, blank=True)
    add_date = models.DateTimeField(auto_now_add=True)
    main_image = models.ForeignKey('ProductImage', related_name='prod', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()
    active_product = ActiveProductManager()

    def get_comments(self):
        return self.productcomment_set.all().select_related('user').order_by('created')

    def get_nmb_of_rating(self):
        return self.productrating_set.all().count()

    def get_avg_rating_in_px(self):
        avg = self.average_rating if self.average_rating else 0
        return WIDTH_OF_RATING_STAR*avg

    def get_not_main_images(self):
        return self.images.filter(is_main=False)

    def save(self, *args, **kwargs):
        self.average_rating = self.productrating_set.all().aggregate(Avg('rating'))['rating__avg']
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('product:product_detail', args=[str(self.id)])

    def __str__(self):
        return "%s" % self.name


class ProductInCart(models.Model):
    product = models.ForeignKey(Product, related_name='product_in_cart')
    pcs = models.PositiveIntegerField()
    user = models.ForeignKey(User, related_name='product_in_cart', blank=True, null=True, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, blank=True, null=True, on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now_add=True)
    objects = CartManager.from_queryset(CartQuerySet)()

    def get_total_price(self):
        return self.product.price*self.pcs

    def save(self, *args, **kwargs):
        try:
            product = ProductInCart.objects.get(product=self.product,
                                                user=self.user, session=self.session)
            product.pcs += self.pcs
            super(ProductInCart, product).save(*args, **kwargs)
        except ProductInCart.DoesNotExist:
            super(ProductInCart, self).save(*args, **kwargs)


class ProductRating(models.Model):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    rating = models.CharField(max_length=6, default='0')

    class Meta:
        unique_together = ('product', 'user')


class ProductComment(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    text = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, blank=True, related_name='images')
    image = models.ImageField(upload_to='products_images/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        main = '(Головна)' if self.is_main else ''
        return "%s... %s" % (self.product.name[:15], main)

from .signals import save_product