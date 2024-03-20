from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Review
from .models import CustomUser

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput()
        }



class ReviewEditForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']