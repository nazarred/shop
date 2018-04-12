from django import forms
from django.forms import Textarea
from .models import ProductRating, ProductComment, ProductInCart, Product


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


class ProductInCartForm(forms.ModelForm):

    class Meta:
        model = ProductInCart
        fields = ['pcs']


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []

    # def __init__(self, *args, **kwargs):
    #     super(ProductModelForm, self).__init__(*args, **kwargs)
    #     instance = kwargs.get('instance')
    #     if not instance:
    #         self.Meta.exclude.append('main_image')
    #     else:
    #         super(ProductModelForm, self).__init__(*args, **kwargs)
