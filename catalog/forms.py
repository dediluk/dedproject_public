from django.contrib.auth.forms import UserCreationForm

from .models import *
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


class MyForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Обязательно')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class CreateBookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'image',
            'pages'
        ]
        # widgets = {
        #     'title': forms.TextInput(attrs={
        #         'rows': 2,
        #         'placeholder': 'Название'
        #     }),
        #     'pages': forms.IntegerField(
        #
        #     )
        # }
