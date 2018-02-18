from django.shortcuts import render, redirect
from .models import *
from .forms import RatingModelForm, CommentModelForm
from django.contrib import messages, auth

NMB_OF_PRODUCT = 6


def logout(request):
    auth.logout(request)
    return redirect('/')


def login(request):
    username = request.POST.get('login', '')
    password = request.POST.get('password', '')
    print(request.POST)
    if request.method == 'POST' and username and password:
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Ви успішно авторизовані')
            return redirect('/')
        else:
            messages.error(request, 'Невірний логін або пароль')
    return redirect('/')


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
    comments = ProductComment.objects.filter(product=product)
    if request.method == 'POST':
        if request.POST.get('rating', None):
            form = RatingModelForm(request.POST, instance=product)
            if form.is_valid():
                item = form.save(commit=False)
                item.rating_change()
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
