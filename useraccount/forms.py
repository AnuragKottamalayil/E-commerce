from django.db import models
from django.forms.models import ModelForm
from .models import CustomerOtp, LoginTable
from django import forms
from django.forms import fields,widgets

class RegisterForm(forms.ModelForm):
    class Meta:
        model = LoginTable
        fields = ('first_name','last_name','username','email','phone_no','password')
        help_texts = {'username':None}
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone No'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            
        }

        labels = {
            "first_name": "",
            "last_name": "",
            "username": "",
            "email": "",
            "phone_no": "",
            "password": "",
          
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
class ForgotPasswordForm(forms.ModelForm):
    class Meta:
        model = LoginTable
        fields = ('email',)
        help_texts = {'email':None}
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control forgot', 'placeholder': 'Email Id', 'name': 'email', 'required':""}),
        }
        labels = {
            "email": ""   
        }
class VerifyOtpForm(forms.ModelForm):
    class Meta:
        model = CustomerOtp
        fields = ('otp',)
        help_texts = {'otp':None}
        widgets = {
            'otp': forms.TextInput(attrs={'class': 'form-control forgot', 'placeholder': '4 digit OTP', 'name': 'otp'}),
        }
        labels = {
            "otp": ""   
        }
class ResetPasswordForm(forms.ModelForm):
    class Meta:
        model = LoginTable
        fields = ('password',)
        help_texts = {'password':None}
        widgets = {
            'password': forms.TextInput(attrs={'class': 'form-control forgot', 'placeholder': 'New password', 'name': 'password'}),
        }
        labels = {
            "password": ""   
        }

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = LoginTable
        fields = ('first_name','last_name','username','email','phone_no')
        help_texts = {'username':None}
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone No'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            
        }

        labels = {
            "first_name": "",
            "last_name": "",
            "username": "",
            "email": "",
            "phone_no": "",
            "password": "",
            
        }