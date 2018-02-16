from django.shortcuts import render
from .models import *


def product_list(request):
    products = Product.objects.all()[:5]
    sort = request.GET.get('sort', 'name')
    products_image = ProductImage.objects.filter(is_main=True).order_by('product__%s' % sort)
    return render(request, 'main_page.html', locals())


def product_detail(request, pk):
    return render(request, 'main_page.html')