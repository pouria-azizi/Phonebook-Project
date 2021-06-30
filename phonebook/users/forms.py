from django import forms


class LoginForm(forms.Form):
    """
    The Login Form
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
