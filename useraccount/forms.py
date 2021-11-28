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

class LoginForm(forms.ModelForm):
    class Meta:
        model = LoginTable
        fields = ('username','password')

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = LoginTable
        fields = ('first_name','last_name','username','email','phone_no','address','zipcode')
        help_texts = {'username':None}