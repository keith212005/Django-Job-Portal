# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from authentication.models import CustomUser


class LoginForm(forms.Form):
  email = forms.CharField(
    widget=forms.TextInput(
      attrs={
        "class": "form-control",
        "placeholder":"email",
      }
    ))
  password = forms.CharField(
    widget=forms.PasswordInput(
      attrs={
        "class": "form-control",
        "placeholder":"password",
      }
    ))


class SignUpForm(UserCreationForm):
  CHOICES = [('2', 'Student'), ('3', 'Company')]
  username = forms.CharField(widget=forms.TextInput(
    attrs={
      "class": "form-control",
      "placeholder": "Username",
    }
  ))

  user_type = forms.IntegerField(
    widget=forms.Select(attrs={'class': 'dropdown-menu dropdown-menu-left show col-md-12'}, choices=CHOICES))

  email = forms.EmailField(
    widget=forms.EmailInput(
      attrs={
        "class": "form-control",
        "placeholder": "email",
      }
    ))
  password1 = forms.CharField(
    widget=forms.PasswordInput(
      attrs={
        "class": "form-control",
        "placeholder": "password",
      }
    ))
  password2 = forms.CharField(
    widget=forms.PasswordInput(
      attrs={
        "class": "form-control",
        "placeholder": "Confirm password",
      }
    ))

  class Meta:
    model = CustomUser
    fields = ('email','username', 'user_type', 'email', 'password1', 'password2')
