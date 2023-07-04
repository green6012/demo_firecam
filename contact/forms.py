from django import forms
from .models import contactform

# class contact_form(forms.ModelForm):
#     class Meta:
#         model = contactform
#         fields = ['username','email','body']

#cach 2
class contact_form(forms.Form):
    username = forms.CharField(max_length=25)
    email = forms.EmailField()
    body = forms.CharField(widget=forms.Textarea)

