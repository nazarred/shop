from django.shortcuts import render
from .models import *
from .forms import RatingModelForm
from django.contrib import messages

NMB_OF_PRODUCT = 6


def product_list(request):
    sort = request.GET.get('sort', 'name')
    products_image = ProductImage.objects.filter(is_main=True).order_by('product__%s' % sort)[:NMB_OF_PRODUCT]
    if request.GET.get('reverse', ''):
        products_image = products_image.reverse()
    return render(request, 'main_page.html', locals())


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    images = ProductImage.objects.filter(product=product, is_main=False)
    main_image = ProductImage.objects.get(product=product, is_main=True)
    form = RatingModelForm()
    if request.method == 'POST':
        if request.POST.get('rating', None):
            form = RatingModelForm(request.POST, instance=product)
            if form.is_valid():
                item = form.save(commit=False)
                item.rating_change()
                messages.success(request, 'Ваша оінка врахована')
    return render(request, 'product/product_detail.html', locals())
