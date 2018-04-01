import logging
from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from profile.models import Profile
from .forms import UserRegistrationForm, ProfileForm
from .mixins import NotLoginRequiredMixin, UserValidMixin

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
    redirect_page = request.GET.get('page', '/')
    auth.logout(request)
    return redirect(redirect_page)


def login(request):
    redirect_page = request.GET.get('page', '/')
    username = request.POST.get('login', '')
    password = request.POST.get('password', '')
    if request.method == 'POST' and username and password:
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Ви успішно авторизовані')
            return redirect(redirect_page)
        else:
            messages.error(request, 'Невірний логін або пароль')
    return redirect(redirect_page)


class ProfileDetailView(LoginRequiredMixin, UserValidMixin, DetailView):
    template_name = 'profile/profile_detail.html'

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UserValidMixin, UpdateView):
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'profile/update_form.html'

    def get_success_url(self):
        return reverse('profile:detail', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data()
        try:
            context['profile'] = self.object.profile
        except Profile.DoesNotExist:
            context['profile'] = None
        context['profile_form'] = ProfileForm(instance=context['profile'])
        return context

    def form_valid(self, form):
        profile = self.get_context_data()['profile']
        profile_form = ProfileForm(self.request.POST, instance=profile)
        if profile_form.is_valid():
            if profile:
                profile_form.save()
            else:
                new_profile = profile_form.save(commit=False)
                new_profile.user = self.object
                new_profile.save()
            messages.success(self.request, 'Updated')
            return super(ProfileUpdateView, self).form_valid(form)
        else:
            messages.warning(self.request, 'Введіть коректно "Номер телефону" і "Дата народження"')
            return super(ProfileUpdateView, self).form_invalid(form)


class PasswordUpdateView(LoginRequiredMixin, UserValidMixin, UpdateView):
    form_class = PasswordChangeForm
    template_name = 'profile/password_update_form.html'
    success_url = reverse_lazy('product_list')

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super(PasswordUpdateView, self).get_form_kwargs()
        kwargs['user'] = kwargs.pop('instance')
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Password updated, sign in')
        return super(PasswordUpdateView, self).form_valid(form)
