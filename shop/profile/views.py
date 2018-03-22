import logging
from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.views.generic import CreateView

from .forms import UserRegistrationForm, ProfileForm
from .mixins import NotLoginRequiredMixin

logger = logging.getLogger(__name__)


class RegisterView(NotLoginRequiredMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'profile/register.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile_form'] = ProfileForm()
        return context

    def form_valid(self, form):
        profile_form = ProfileForm(self.request.POST)
        new_user = form.save(commit=False)
        if profile_form.is_valid():
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            my_password = form.cleaned_data['password']
            user = authenticate(username=new_user.username, password=my_password)
            if user is not None:
                auth.login(self.request, user)
            else:
                logger.warning('User is None!')
            new_profile = profile_form.save(commit=False)
            new_profile.user = user
            new_profile.save()
            messages.success(self.request, 'Ви успішно зареєстровані та авторизовані')
            return super(RegisterView, self).form_valid(form)
        else:
            messages.warning(self.request, 'Введіть коректно "Номер телефону" і "Дата народження"')
            return super(RegisterView, self).form_invalid(form)


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

# def register(request):
#     if request.user.is_authenticated():
#         messages.error(request, 'Ви вже зареєстровані')
#         return redirect('product_list')
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         # form = UserCreationForm(request.POST)
#         profile_form = ProfileForm(request.POST)
#         if form.is_valid() and profile_form.is_valid():
#             new_user = form.save(commit=False)
#             new_user.set_password(form.cleaned_data['password'])
#             new_user.save()
#             # new_user.groups = ['1']  # присвоюється група "Покупці"
#             my_password = form.cleaned_data['password']
#             user = authenticate(username=new_user.username, password=my_password)
#             if user is not None:
#                 auth.login(request, user)
#             new_profile = profile_form.save(commit=False)
#             new_profile.user = user
#             new_profile.save()
#             messages.success(request, 'Ви успішно зареєстровані та авторизовані')
#             return redirect('product_list')
#     else:
#         form = UserRegistrationForm()
#         # form = UserCreationForm(request.POST)
#         profile_form = ProfileForm()
#     return render(request, 'profile/register.html', locals())
