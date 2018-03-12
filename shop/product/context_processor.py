from .models import ProductInCart


def getting_cart_info(request):

    session_key = request.session.session_key
    if not session_key:
        request.session["session_key"] = 123
        request.session.cycle_key()
    products_in_cart = ProductInCart.objects.user_cart(request).select_related('product__main_image', 'user')
    product_in_cart_pcs = ProductInCart.objects.user_cart(request).count()
    return locals()
