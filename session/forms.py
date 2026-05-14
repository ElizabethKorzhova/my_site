"""This module contains all forms for session application."""
from django import forms


class LoginForm(forms.Form):
    """Form for logging."""
    name = forms.CharField(max_length=100)
    age = forms.IntegerField(min_value=1, max_value=120)
