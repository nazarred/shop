from django import forms
from .models import *


class RatingModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['rating']
