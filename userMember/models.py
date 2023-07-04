from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.forms import  UserCreationForm

# Create your models here.

#chane register form
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

