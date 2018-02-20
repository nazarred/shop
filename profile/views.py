from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import *


def register(request):
    if request.user.is_authenticated():
        messages.error(request, 'Ви вже зареєстровані')
        return redirect('product_list')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        # form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            new_user.groups = ['1']  # присвоюється група "Покупці"
            new_user.save()
            my_password = form.cleaned_data.get('password1')
            user = authenticate(username=new_user.username, password=my_password)
            if user is not None:
                auth.login(request, user)
            new_profile = profile_form.save(commit=False)
            new_profile.user = user
            new_profile.save()
            messages.success(request, 'Ви успішно зареєстровані та авторизовані')
            return redirect('product_list')
    else:
        form = UserRegistrationForm()
        # form = UserCreationForm(request.POST)
        profile_form = ProfileForm()
    return render(request, 'profile/register.html', locals())


# def detail_register(request, pk):
#     user = User.objects.get(id=pk)
#     if request.method == 'POST':
#         form = ProfileForm(request.POST)
#         if form.is_valid():
#             new_profile = form.save(commit=False)
#             new_profile.user = request.user
#             new_profile.save()
#             return redirect('product_list')
#     else:
#         form = ProfileForm()
#     return render(request, 'profile/detail_register.html', locals())
