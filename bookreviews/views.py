import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, login, logout

from .models import Commenting
from .models import CustomUser
from .models import Review

from .forms import ReviewForm
from .forms import RegistrationForm
from .forms import CommentForm
from .forms import SearchForm
from .forms import UserEditForm
from .forms import CombinedSearchForm

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib import messages
from django.urls import reverse


#### admin panel functions #####


@login_required
@permission_required("bookreviews.can_access_admin_panel")
def admin_panel(request):
    """Function to display admin panel template to site admins."""
    return render(request, "admin_panel.html")


@login_required
@permission_required("bookreviews.can_view_user_details_in_admin_panel")
def user_detail(request, user_id):
    """Function to display user details."""
    user = get_object_or_404(CustomUser, pk=user_id)
    return render(request, "user_detail.html", {"user": user})


@login_required
@permission_required("bookreviews.can_search_users_in_admin_panel")
def search_users_reviews(request):
    """Function to search users and reviews by site admins."""
    form = CombinedSearchForm(request.GET)
    users = []
    reviews = []
    comments = []

    if form.is_valid():
        username = form.cleaned_data.get("username")
        review_content = form.cleaned_data.get("review_content")
        comment_text = form.cleaned_data.get("comment_text")

        if username:
            users = CustomUser.objects.filter(username__icontains=username)

        if review_content:
            reviews = Review.objects.filter(review_content__icontains=review_content)

        if comment_text:
            comments = Commenting.objects.filter(comment_text__icontains=comment_text)

    return render(
        request,
        "search_users_reviews.html",
        {"form": form, "users": users, "reviews": reviews, "comments": comments},
    )


@login_required
@permission_required("bookreviews.can_edit_reviews")
def edit_any_review(request, review_id):
    """Function to allow site admins to edit any review."""
    review = get_object_or_404(Review, id=review_id)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "The review has been edited successfully.")
            return redirect("book_detail", book_id=review.book_id)
    else:
        form = ReviewForm(instance=review)

    book_data = {
        "id": review.book_id,
        "title": review.book_title,
        "author": review.book_author,
        "description": review.book_description,
        "category": review.book_category,
        "image": review.book_image,
    }
    return render(request, "edit_any_review.html", {"form": form, "book": book_data})


@login_required
@permission_required("bookreviews.can_delete_reviews")
def delete_any_review(request, review_id):
    """Function to allow site admins to delete any review."""
    review = get_object_or_404(Review, id=review_id)
    if request.method == "POST" and request.POST.get("delete_any_review") == "yes":
        book_id = review.book_id
        review.delete()
        messages.success(request, "Your review has been deleted successfully.")
        return redirect("book_detail", book_id=book_id)
    else:

        return render(request, "delete_any_review.html", {"review": review})


@login_required
@permission_required("bookreviews.can_delete_comments")
def delete_comment(request, comment_id):
    """Function to allow site admins to delete any comment made on a review."""
    comment = get_object_or_404(Commenting, pk=comment_id)
    book_id = comment.review.book_id
    if request.method == "POST":
        comment.delete()
        messages.success(request, "The comment has been deleted successfully.")
    return redirect("book_detail", book_id=book_id)


@login_required
@permission_required("bookreviews.can_view_users")
def list_users(request):
    """Function to list all users by site admins."""
    if not request.user.has_perm("bookreviews.can_view_users"):
        pass
    users = CustomUser.objects.all()
    total_users = CustomUser.objects.count()
    return render(
        request, "list_users.html", {"users": users, "total_users": total_users}
    )


@login_required
@permission_required("bookreviews.can_edit_user")
def edit_user(request, user_id):
    """Function to edit user by site admins."""
    if not request.user.has_perm("bookreviews.can_edit_user"):
        pass

    admin = request.user
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User edited successfully.")
            return redirect("user_detail", user_id=user_id)
    else:
        form = UserEditForm(instance=user)

    return render(
        request, "edit_user.html", {"form": form, "user": user, "admin": admin}
    )


@login_required
@permission_required("bookreviews.can_delete_users")
def delete_user(request, user_id):
    """Function to delete user by site admins."""
    if request.method == "POST":
        user = get_object_or_404(CustomUser, pk=user_id)
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect("admin_panel")
    else:
        user = get_object_or_404(CustomUser, pk=user_id)
        return render(request, "delete_user_confirm.html", {"user": user})


@login_required
@permission_required("bookreviews.can_view_all_reviews")
def total_reviews(request):
    """Function to display total number of reviews for site admins."""
    total_reviews = Review.objects.count()
    return render(request, "total_reviews.html", {"total_reviews": total_reviews})


###### End of Admin Panel Functions ######


def edit_review(request, review_id):
    """Function to edit a review."""
    review = get_object_or_404(Review, id=review_id)
    if review.user == request.user:
        if request.method == "POST":
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, "Your review has been edited successfully.")
                return redirect("book_detail", book_id=review.book_id)
        else:
            form = ReviewForm(instance=review)
        book_data = {
            "id": review.book_id,
            "title": review.book_title,
            "author": review.book_author,
            "description": review.book_description,
            "category": review.book_category,
            "image": review.book_image,
        }
        return render(request, "edit_review.html", {"form": form, "book": book_data})
    else:
        return HttpResponseForbidden("You are not authorized to edit this review.")


def delete_review(request, review_id):
    """Function to delete a review."""
    review = get_object_or_404(Review, id=review_id)
    if review.user == request.user:
        if request.method == "POST" and request.POST.get("confirm_delete"):
            book_id = review.book_id
            review.delete()
            messages.success(request, "Your review has been deleted successfully.")
            return redirect("book_detail", book_id=book_id)
        else:

            return render(request, "confirm_delete_review.html", {"review": review})
    else:
        return HttpResponseForbidden("You are not authorized to delete this review.")


def user_login(request):
    """Function to log in the user."""
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def user_logout(request):
    """Function to log out the user."""
    logout(request)
    return redirect("index")


def register(request):
    """Fucntion to register a new user."""
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "register.html", {"form": form})


@login_required
def my_reviews(request):
    """Display all of the user's reviews."""
    user_reviews = Review.objects.filter(user=request.user)
    reviews_with_books = []

    for review in user_reviews:
        book_data = {
            "title": review.book_title,
            "author": review.book_author,
            "description": review.book_description,
            "category": review.book_category,
            "image": review.book_image,
        }

        reviews_with_books.append({"review": review, "book": book_data})

    return render(
        request, "my_reviews.html", {"reviews_with_books": reviews_with_books}
    )


def index(request):
    """View function for home page of site."""
    google_book_api = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": "subject:science fiction|classic|crime and mystery|fantasy|true crime|Fiction",
        "maxResults": 40,
    }

    response = requests.get(google_book_api, params=params).json()

    books = []
    for data in response["items"]:
        info = data["volumeInfo"]
        book_data = {
            "id": data["id"],  # Use Google Books API book ID as the identifier
            "title": info["title"],
            "author": info.get("authors", ["Author Not Available"])[0],
            "description": info.get("description", "No Description"),
            "category": info.get("categories", ["No Categories"])[0],
            "image": info.get("imageLinks", {}).get(
                "thumbnail", "https://islandpress.org/files/default_book_cover_2015.jpg"
            ),
        }
        books.append(book_data)

    context = {"books": books}
    return render(request, "index.html", context)


def book_detail(request, book_id):
    """Function to display book details"""
    google_book_api = "https://www.googleapis.com/books/v1/volumes/{}".format(book_id)
    response = requests.get(google_book_api).json()

    if "error" in response:
        return HttpResponseNotFound("Book not found")

    info = response["volumeInfo"]
    book_data = {
        "id": response["id"],
        "title": info["title"],
        "author": info.get("authors", ["Author Not Available"])[0],
        "description": info.get("description", "No Description"),
        "category": info.get("categories", ["No Categories"])[0],
        "image": info.get("imageLinks", {}).get(
            "thumbnail", "https://islandpress.org/files/default_book_cover_2015.jpg"
        ),
        "reviews": Review.objects.filter(book_id=book_id),
    }

    comment_form = CommentForm()
    return render(
        request,
        "book_detail.html",
        {
            "book": book_data,
            "reviews": book_data["reviews"],
            "comment_form": comment_form,
        },
    )


def leave_review(request, book_id):
    """Function to leave a book review."""
    google_book_api = "https://www.googleapis.com/books/v1/volumes/{}".format(book_id)
    response = requests.get(google_book_api).json()

    if "error" in response:
        return HttpResponseNotFound("Book not found")

    info = response["volumeInfo"]
    book_data = {
        "id": response["id"],
        "title": info["title"],
        "author": info.get("authors", ["Author Not Available"])[0],
        "description": info.get("description", "No Description"),
        "category": info.get("categories", ["No Categories"])[0],
        "image": info.get("imageLinks", {}).get(
            "thumbnail", "https://islandpress.org/files/default_book_cover_2015.jpg"
        ),
    }

    if not request.user.is_authenticated:
        messages.info(request, "You need to log in to leave a review.")
        return redirect("login")

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book_id = book_data["id"]
            review.book_title = book_data["title"]  # Associate book title with review
            review.book_author = book_data["author"]
            review.book_description = book_data["description"]
            review.book_category = book_data["category"]
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been submitted successfully.")
            return redirect("book_detail", book_id=book_id)
    else:
        form = ReviewForm()

    return render(request, "leave_review.html", {"form": form, "book": book_data})


@login_required
def add_comment_to_review(request, review_id):
    """Function to add a comment to a review."""
    review = get_object_or_404(Review, pk=review_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.review = review
            comment.save()
            messages.success(request, "Your comment has been added successfully.")
    return redirect("book_detail", book_id=review.book_id)


def search_books(request):
    """Function to search books on Google Books API."""
    form = SearchForm(request.GET)
    books = []

    if form.is_valid():
        query = form.cleaned_data["query"]
        category = form.cleaned_data.get("category")

        google_books_api = (
            f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=40"
        )
        if category:
            google_books_api += f"&subject={category}"

        response = requests.get(google_books_api).json()

        if "items" in response:
            for item in response["items"]:
                book_data = {
                    "id": item["id"],
                    "title": item.get("volumeInfo", {}).get(
                        "title", "Title Not Available"
                    ),
                    "author": item.get("volumeInfo", {}).get(
                        "authors", ["Author Not Available"]
                    )[0],
                    "description": item.get("volumeInfo", {}).get(
                        "description", "Description Not Available"
                    ),
                    "category": item.get("volumeInfo", {}).get(
                        "categories", ["Category Not Available"]
                    )[0],
                    "image": item.get("volumeInfo", {})
                    .get("imageLinks", {})
                    .get(
                        "thumbnail",
                        "https://islandpress.org/files/default_book_cover_2015.jpg",
                    ),
                }
                books.append(book_data)

    return render(request, "search_results.html", {"form": form, "books": books})


def review_detail(request, review_id):
    """Function to display review details."""
    review = get_object_or_404(Review, id=review_id)
    book_title = review.book_title
    book_author = review.book_author
    book_description = review.book_description
    book_category = review.book_category
    return render(
        request,
        "review_detail.html",
        {
            "review": review,
            "book_title": book_title,
            "book_author": book_author,
            "book_description": book_description,
            "book_category": book_category,
        },
    )
