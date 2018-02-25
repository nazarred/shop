from django.contrib import messages, auth
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import CommentModelForm
from .models import Product, ProductComment, ProductRating, ProductImage

NMB_OF_PRODUCT = 6


def product_list(request):
    sort = request.GET.get('sort', 'name')
    # products = Product.objects.all().order_by('%s' % sort).prefetch_related('images')[:NMB_OF_PRODUCT]
    products_images = ProductImage.objects.filter(is_main=True).order_by('product__%s' % sort).select_related('product')[:NMB_OF_PRODUCT]
    if request.GET.get('reverse', ''):
        products_images = products_images.reverse()
    return render(request, 'main_page.html', locals())


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    comments = ProductComment.objects.filter(product=product).select_related('user')
    if request.POST.get('text', None):
        comment_form = CommentModelForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()
        return redirect('product:product_detail', pk=product.id)
    else:
        comment_form = CommentModelForm()
    return render(request, 'product/product_detail.html', locals())


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
