from django.db import models
from django.forms.models import ModelForm
from .models import LoginTable
from django import forms
from django.forms import fields,widgets

class RegisterForm(forms.ModelForm):
    class Meta:
        model = LoginTable
        fields = ('first_name','last_name','username','email','phone_no','password','address','zipcode')
        help_texts = {'username':None}
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone No'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'})
        }

        labels = {
            "first_name": "",
            "last_name": "",
            "username": "",
            "email": "",
            "phone_no": "",
            "password": "",
            "address": "",
            "zipcode": "",
        }

class LoginForm(forms.ModelForm):
    class Meta:
        model = LoginTable
        fields = ('username','password')
        help_texts = {'username':None}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }
        labels = {
            "username": "",
            "password": "",
        }

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = LoginTable
        fields = ('first_name','last_name','username','email','phone_no','address','zipcode')
        help_texts = {'username':None}
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone No'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'})
        }

        labels = {
            "first_name": "",
            "last_name": "",
            "username": "",
            "email": "",
            "phone_no": "",
            "password": "",
            "address": "",
            "zipcode": "",
        }