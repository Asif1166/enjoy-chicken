from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserRegistrationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email']