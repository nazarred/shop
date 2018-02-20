from django.contrib import messages, auth
from django.shortcuts import render

from .forms import *

NMB_OF_PRODUCT = 6


def product_list(request):
    sort = request.GET.get('sort', 'name')
    products = Product.objects.all().order_by('%s' % sort)[:NMB_OF_PRODUCT]
    if request.GET.get('reverse', ''):
        products = products.reverse()
    return render(request, 'main_page.html', locals())


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    comments = ProductComment.objects.filter(product=product)
    if request.method == 'POST':
        if request.POST.get('rating', None):
            form = RatingModelForm(request.POST)
            if form.is_valid():
                rating = form.save(commit=False)
                rating.product = product
                rating.user = auth.get_user(request)
                rating.save()
                product.save()
                messages.success(request, 'Ваша оінка врахована')
        if request.POST.get('text', None):
            comment_form = CommentModelForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.product = product
                comment.save()
    else:
        form = RatingModelForm()
    comment_form = CommentModelForm()
    return render(request, 'product/product_detail.html', locals())
