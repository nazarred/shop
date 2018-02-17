from django.shortcuts import render
from .models import *

NMB_OF_PRODUCT = 6


def product_list(request):
    sort = request.GET.get('sort', 'name')
    products_image = ProductImage.objects.filter(is_main=True).order_by('product__%s' % sort)[:NMB_OF_PRODUCT]
    if request.GET.get('reverse', ''):
        products_image = products_image.reverse()
    return render(request, 'main_page.html', locals())


def product_detail(request, pk):
    return render(request, 'main_page.html')