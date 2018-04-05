import logging
from django.contrib import messages, auth
from django.http import JsonResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView

from .forms import CommentModelForm, ProductInCartForm
from .models import Product, ProductRating, ProductInCart
from .utils import get_session_instance

logger = logging.getLogger(__name__)

PRODUCTS_ON_PAGE = 3


class ProductsList(ListView):
    model = Product
    template_name = 'main_page.html'
    context_object_name = 'products'
    paginate_by = PRODUCTS_ON_PAGE
    queryset = model.active_products.all().select_related('main_image')

    def get_queryset(self):
        qs = super().get_queryset()
        sort = self.request.GET.get('sort', 'name')
        qs = qs.order_by('%s' % sort)
        print(self.request.session.model)
        if self.request.GET.get('reverse', None):
            qs = qs.reverse()
        return qs

    def get_context_data(self, **kwargs):
        context = super(ProductsList, self).get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort', 'name')
        context['reverse'] = self.request.GET.get('reverse', '')
        return context


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentModelForm()
        context['cart_form'] = ProductInCartForm()
        if self.request.user.is_authenticated():
            try:
                context['user_rating'] = self.object.productrating_set.get(user=self.request.user)
            except ProductRating.DoesNotExist:
                pass
        return context


def comments(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentModelForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()
    return redirect(product.get_absolute_url())


def rating_change(request, pk):
    return_dict = {}
    product = Product.objects.get(id=pk)
    try:
        rating = ProductRating.objects.create(user=auth.get_user(request),
                                              rating=request.POST['click_rating'], product=product)
        return_dict['avg_rating'] = product.average_rating
        return_dict['r_rating'] = rating.rating
        return_dict['px_rating'] = product.get_avg_rating_in_px()
    except Exception:
        messages.error(request, 'Ви вже голосували')

    return JsonResponse(return_dict)


class ProductsCartView(ListView):
    model = ProductInCart
    template_name = 'product/product_cart.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.user_cart(self.request)
        qs = qs.order_by('add_date').select_related('product__main_image', 'user')
        return qs


def add_product_in_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        cart_form = ProductInCartForm(request.POST)
        if cart_form.is_valid():
            cart = cart_form.save(commit=False)
            cart.product = product
            if request.user.is_authenticated:
                cart.user = request.user
            else:
                session = get_session_instance(request)  # можливо є і інший спосіб, але я його ще не знайшов
                if not session:
                    logger.warning('session is not created')
                    raise Http404
                cart.session = session
            product_in_cart, created = ProductInCart.objects.get_or_create(
                user=cart.user,
                session=cart.session,
                product=product,
                defaults={'pcs': cart.pcs}
            )
            if not created:
                product_in_cart.increment_pcs(cart.pcs)
            messages.success(request, 'Продукт успішно добавлений')
    return redirect(product.get_absolute_url())


class DeleteProductsFromCartView(DeleteView):
    model = ProductInCart
    success_url = reverse_lazy('product:product_in_cart')
