from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import Book, Review
from .forms import ReviewForm
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Review


def index(request):
    books = Book.objects.all()
    return render(request, 'index.html', {'books': books})


def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    reviews = Review.objects.filter(book=book)
    return render(request, 'book_detail.html', {'book': book, 'reviews': reviews})








def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



def user_logout(request):
    logout(request)
    return redirect('index')



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create a new CustomUser instance
            user = form.save(commit=False)
            # Set the password for the user

             #   user.set_password(form.cleaned_data['password'])

            # Save the user object with the hashed password
            user.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

