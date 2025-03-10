from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ProfileDetails

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','username', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileDetails
        fields = ['Profile_Image', 'NamesUser', 'Channel_Name', 'uName']
