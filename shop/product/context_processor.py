
from .models import ProductInCart


def getting_cart_info(request):

    session_key = request.session.session_key
    if not session_key:
        request.session["session_key"] = 123
        request.session.cycle_key()
    if request.user.is_authenticated:
        product_in_cart_pcs = ProductInCart.objects.filter(user=request.user).count()
    else:
        product_in_cart_pcs = ProductInCart.objects.filter(session_key=session_key).count()
    print(product_in_cart_pcs)
    return locals()
