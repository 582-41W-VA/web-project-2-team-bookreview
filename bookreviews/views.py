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


def index(request):
    books = Book.objects.all()
    return render(request, 'index.html', {'books': books})


def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    reviews = Review.objects.filter(book=book)
    return render(request, 'book_detail.html', {'book': book, 'reviews': reviews})


# @login_required
def leave_review(request, book_id):
    if not request.user.is_authenticated:
        login_url = reverse('login')
        login_link = f'<a class="login-link" href="{login_url}">Log in</a>'
        register_link = f'<a class="register-link" href="{reverse("register")}">Register</a>'
        messages.info(request, f'You need to log in to leave a review. Please {login_link} or {register_link}.')
        return redirect('login')
    else:
        book = get_object_or_404(Book, id=book_id)
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.book = book  # Assign the current book to the review
                review.user = request.user  # Assign the logged-in user to the review
                review.save()
                messages.success(request, 'Your review has been submitted successfully.')
                return redirect('book_detail', book_id=book.id)  # Redirect to the book detail page
        else:
            form = ReviewForm()
        return render(request, 'leave_review.html', {'form': form, 'book': book})
    




def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user == request.user:  # Check if the logged-in user owns the review
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your review has been edited successfully.')
                return redirect('book_detail', book_id=review.book.id)  # Redirect to user's reviews page
        else:
            form = ReviewForm(instance=review)
        return render(request, 'edit_review.html', {'form': form, 'book': review.book})
    else:
        return HttpResponseForbidden("You are not authorized to edit this review.")




def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user == request.user:  # Check if the logged-in user owns the review
        if request.method == 'POST' and request.POST.get('confirm_delete'):
            review.delete()
            messages.success(request, 'Your review has been deleted successfully.')
            return redirect('book_detail', book_id=review.book.id)  # Redirect to book detail page after deletion
        else:
            return render(request, 'confirm_delete_review.html', {'review': review})
    else:
        return HttpResponseForbidden("You are not authorized to delete this review.")



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

