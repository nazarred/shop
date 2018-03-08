from django.utils import timezone
from django import forms
from django.contrib.auth import password_validation
from django.forms import SelectDateWidget
from django.contrib.auth.models import User
from .models import Profile


class ProfileForm(forms.ModelForm):
    years = range(1900, timezone.now().year+1)
    months = {
        1: 'Січень', 2: 'Лютий', 3: 'Березень', 4: 'Квітень',
        5: 'Травень', 6: 'Червень', 7: 'Липень', 8: 'Серпень',
        9: 'Вересень', 10: 'Жовтень', 11: 'Листопад', 12: 'Грудень'
    }
    date_of_birth = forms.DateField(widget=SelectDateWidget(months=months, years=years))

    class Meta:
        model = Profile
        fields = ('phone_nmb', 'date_of_birth')


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password1 = forms.CharField(label='Повторіть пароль', widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password1(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password1']:
            raise forms.ValidationError('Паролі не співпадають')
        # self.instance.username = self.cleaned_data['username']
        password_validation.validate_password(self.cleaned_data['password1'], self.instance)
        return cd['password']



