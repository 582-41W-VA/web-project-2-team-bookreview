from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Review
from .models import CustomUser
from .models import Commenting

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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Commenting
        fields = ['comment_text']
        widgets = {
            'comment_text': forms.Textarea(attrs={'cols': 60, 'rows': 2})  # Adjust the cols and rows as needed   
        }


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
    fields = ['search']
