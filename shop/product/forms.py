from django import forms
from django.forms import Textarea
from .models import ProductRating, ProductComment


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
