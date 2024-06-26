from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Review
from .models import CustomUser
from .models import Commenting
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class ReviewForm(forms.ModelForm):
    review_content = forms.CharField(widget=SummernoteWidget())
    class Meta:
        model = Review
        fields = ['rating', 'review_content']


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput()
        }


class ReviewEditForm(forms.ModelForm):
    review_content = forms.CharField(widget=SummernoteWidget())
    class Meta:
        model = Review
        fields = ['rating', 'review_content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Commenting
        fields = ['comment_text']
        widgets = {
            'comment_text': forms.Textarea(attrs={'cols': 40, 'rows': 3})  # Adjust the cols and rows as needed   
        }


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
    fields = ['search']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)


class CombinedSearchForm(forms.Form):
    username = forms.CharField(label='Search for Username', max_length=255, required=False)
    review_content = forms.CharField(label='Search Review Content', max_length=255, required=False)
    comment_text = forms.CharField(label='Search Comment Text', max_length=255, required=False)