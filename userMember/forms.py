from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
class registerForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(max_length=25, widget=forms.PasswordInput)

class loginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=25, widget=forms.PasswordInput)

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}))
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']