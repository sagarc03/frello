"""User forms"""
from django import forms


class LoginForm(forms.Form):
    """Login form"""

    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password")
