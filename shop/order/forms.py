from django import forms
from .models import Order


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['products', 'status', 'user']


