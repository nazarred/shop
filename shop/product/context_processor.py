from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse

from .models import ProductInCart


def getting_cart_info(request):

    session_key = request.session.session_key
    if not session_key:
        # без цього рядка буде помилка при виклику cycle_key()
        # виправленно в нових версіях https://github.com/django/django/commit/887f3d3219b9f8192d27314eceee27ab1f89c5cc
        request.session["session_key"] = None
        request.session.cycle_key()
    products_in_cart = ProductInCart.objects.user_cart(request).select_related('product__main_image', 'user')
    cart_url = reverse('product:product_in_cart')
    if request.path == cart_url:
        paginator_for_cart = Paginator(products_in_cart, 3)
        product_in_cart_pcs = paginator_for_cart.count
        page = request.GET.get('page')
        try:
            products_in_cart = paginator_for_cart.page(page)
        except PageNotAnInteger:
            products_in_cart = paginator_for_cart.page(1)
        except EmptyPage:
            products_in_cart = paginator_for_cart.page(paginator_for_cart.num_pages)
    else:
        product_in_cart_pcs = products_in_cart.count
    return locals()
