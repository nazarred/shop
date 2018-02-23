from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import *
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
    products = Product.objects.all().order_by('%s' % sort)[:NMB_OF_PRODUCT]
    if request.GET.get('reverse', ''):
        products = products.reverse()
    return render(request, '../templates/main_page.html', locals())


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    comments = ProductComment.objects.filter(product=product)
    if request.user.is_authenticated():
        try:
            users_rating = product.productrating_set.get(user=request.user)
        except ProductRating.DoesNotExist:
            users_rating = None
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
        return redirect('product:product_detail', pk=product.id)
    else:
        form = RatingModelForm()
        comment_form = CommentModelForm()
    return render(request, 'product/templates/product/product_detail.html', locals())


def rating_change(request):
    return_dict = {}
    session_key = request.session.session_key
    print(request.POST)
    return JsonResponse(return_dict)
