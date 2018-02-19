from django import forms
from .models import *
from django.forms import Textarea


class RatingModelForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        fields = ['rating']


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['text']

        widgets = {
            'text': Textarea(attrs={'placeholder': 'Ваш коментар...'}),
        }
