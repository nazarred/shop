from .models import ProductInCart


def getting_cart_info(request):

    session_key = request.session.session_key
    if not session_key:
        # без цього рядка буде помилка при виклику cycle_key()
        # виправленно в нових версіях https://github.com/django/django/commit/887f3d3219b9f8192d27314eceee27ab1f89c5cc
        request.session["session_key"] = None
        request.session.cycle_key()
    products_in_cart = ProductInCart.objects.user_cart(request).select_related('product__main_image', 'user')
    product_in_cart_pcs = ProductInCart.objects.user_cart(request).count()
    return locals()
