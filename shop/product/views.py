from django.contrib import messages, auth
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from .forms import CommentModelForm
from .models import Product, ProductComment, ProductRating, ProductImage

NMB_OF_PRODUCT = 6


class ProductsList(ListView):
    model = ProductImage
    template_name = 'main_page.html'
    context_object_name = 'products_images'

    def get_queryset(self):
        qs = super().get_queryset()
        sort = self.request.GET.get('sort', 'name')
        qs = qs.filter(is_main=True).order_by('product__%s' % sort).select_related(
            'product')[:NMB_OF_PRODUCT]
        if self.request.GET.get('reverse', None):
            qs = qs.reverse()
        return qs


# def product_list(request):
#     sort = request.GET.get('sort', 'name')
#     # products = Product.objects.all().order_by('%s' % sort).prefetch_related('images')[:NMB_OF_PRODUCT]
#     products_images = ProductImage.objects.filter(is_main=True).order_by('product__%s' % sort).select_related('product')[:NMB_OF_PRODUCT]
#     if request.GET.get('reverse', ''):
#         products_images = products_images.reverse()
#     return render(request, 'main_page.html', locals())

class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentModelForm()
        if self.request.user.is_authenticated():
            try:
                context['user_rating'] = self.object.productrating_set.get(user=self.request.user)
            except ProductRating.DoesNotExist:
                pass
        return context


def comments(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        comment_form = CommentModelForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()
    return redirect(product.get_absolute_url())


# def product_detail(request, pk):
#     product = Product.objects.get(id=pk)
#     comments = ProductComment.objects.filter(product=product).select_related('user')
#     if request.user.is_authenticated():
#         try:
#             users_rating = product.productrating_set.get(user=request.user)
#         except ProductRating.DoesNotExist:
#             users_rating = None
#     if request.POST.get('text', None):
#         comment_form = CommentModelForm(request.POST)
#         if comment_form.is_valid():
#             comment = comment_form.save(commit=False)
#             comment.user = request.user
#             comment.product = product
#             comment.save()
#         return redirect('product:product_detail', pk=product.id)
#     else:
#         comment_form = CommentModelForm()
#     return render(request, 'product/product_detail.html', locals())


def rating_change(request, pk):
    return_dict = {}
    product = Product.objects.get(id=pk)
    try:
        rating = ProductRating.objects.create(user=auth.get_user(request),
                                              rating=request.POST['click_rating'], product=product)
        product.save()
        return_dict['avg_rating'] = product.average_rating
        return_dict['r_rating'] = rating.rating
        return_dict['px_rating'] = product.get_avg_rating_in_px()
    except Exception:
        messages.error(request, 'Ви вже голосували')

    return JsonResponse(return_dict)


