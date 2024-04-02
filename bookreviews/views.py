import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, login, logout

# from .models import Book
from .models import BookInfo
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

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache


@login_required
@permission_required("bookreviews.can_edit_reviews")
def edit_any_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "The review has been edited successfully.")
            return redirect(
                "book_detail", book_id=review.book_id
            ) 
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
    review = get_object_or_404(Review, id=review_id)
    if request.method == "POST" and request.POST.get("delete_any_review") == "yes":
        book_id = review.book_id  
        review.delete()
        messages.success(request, "Your review has been deleted successfully.")
        return redirect(
            "book_detail", book_id=book_id
        )  
    else:
        
        return render(request, "delete_any_review.html", {"review": review})


@login_required
@permission_required("bookreviews.can_delete_comments")
def delete_comment(request, comment_id):
    comment = get_object_or_404(Commenting, pk=comment_id)
    book_id = comment.review.book_id
    if request.method == "POST":
        comment.delete()
        messages.success(request, "The comment has been deleted successfully.")
    return redirect("book_detail", book_id=book_id)


@permission_required("bookreviews.can_view_users")
def list_users(request):
    if not request.user.has_perm("bookreviews.can_view_users"):
        pass
    users = CustomUser.objects.all()
    total_users = CustomUser.objects.count()
    return render(
        request, "list_users.html", {"users": users, "total_users": total_users}
    )


@permission_required("bookreviews.can_edit_user")
def edit_user(request, user_id):
    if not request.user.has_perm("bookreviews.can_edit_user"):
        pass  

    admin = request.user  
    user = get_object_or_404(CustomUser, pk=user_id)  
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User edited successfully.")
            return redirect(
                "user_detail", user_id=user_id
            )  
    else:
        form = UserEditForm(instance=user)

    return render(
        request, "edit_user.html", {"form": form, "user": user, "admin": admin}
    )


@login_required
@permission_required("bookreviews.can_delete_users")
def delete_user(request, user_id):
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
    total_reviews = Review.objects.count()
    return render(request, "total_reviews.html", {"total_reviews": total_reviews})


#### admin panel #####


@login_required
@permission_required("bookreviews.can_access_admin_panel")
def admin_panel(request):
    return render(request, "admin_panel.html")


User = get_user_model()


@login_required
@permission_required("bookreviews.can_view_user_details_in_admin_panel")
def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    return render(request, "user_detail.html", {"user": user})


@login_required
@permission_required('bookreviews.can_search_users_in_admin_panel')
def search_users_reviews(request):
    form = CombinedSearchForm(request.GET)
    users = []
    reviews = []
    comments = []

    if form.is_valid():
        username = form.cleaned_data.get('username')
        review_content = form.cleaned_data.get('review_content')
        comment_text = form.cleaned_data.get('comment_text')

        if username:
            users = CustomUser.objects.filter(username__icontains=username)

        if review_content:
            reviews = Review.objects.filter(review_content__icontains=review_content)

            for review in reviews:
                try:
                    book_title = BookInfo.objects.get(book_id=review.book_id).book_title
                    review.book_title = book_title
                except BookInfo.DoesNotExist:
                    review.book_title = "Book Title Not Available"

        if comment_text:
            comments = Commenting.objects.filter(comment_text__icontains=comment_text)

    return render(request, 'search_users_reviews.html', {'form': form, 'users': users, 'reviews': reviews, 'comments': comments})



def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user == request.user: 
        if request.method == "POST":
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, "Your review has been edited successfully.")
                return redirect(
                    "book_detail", book_id=review.book_id
                )  
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
    review = get_object_or_404(Review, id=review_id)
    if review.user == request.user: 
        if request.method == "POST" and request.POST.get("confirm_delete"):
            book_id = review.book_id  
            review.delete()
            messages.success(request, "Your review has been deleted successfully.")
            return redirect(
                "book_detail", book_id=book_id
            )  
        else:
            
            return render(request, "confirm_delete_review.html", {"review": review})
    else:
        return HttpResponseForbidden("You are not authorized to delete this review.")


def user_login(request):
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
    logout(request)
    return redirect("index")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #   user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect(
                "login"
            ) 
    else:
        form = RegistrationForm()
    return render(request, "register.html", {"form": form})


@login_required
def my_reviews(request):
    user_reviews = Review.objects.filter(user=request.user)
    reviews_with_books = []

    for review in user_reviews:

        cache_key = f"book_data_{review.book_id}"

        book_data = cache.get(cache_key)

        if not book_data:

            google_book_api = (
                f"https://www.googleapis.com/books/v1/volumes/{review.book_id}"
            )
            response = requests.get(google_book_api).json()

            if "error" not in response:
                info = response["volumeInfo"]
                book_data = {
                    "title": info.get("title", "Title Not Available"),
                    "author": info.get("authors", ["Author Not Available"])[0],
                    "description": info.get("description", "No Description"),
                    "category": info.get("categories", ["No Categories"])[0],
                    "image": info.get("imageLinks", {}).get(
                        "thumbnail",
                        "https://islandpress.org/files/default_book_cover_2015.jpg",
                    ),
                }

                cache.set(
                    cache_key, book_data, timeout=3600
                )  
            else:

                book_data = None

        reviews_with_books.append({"review": review, "book": book_data})

    return render(
        request, "my_reviews.html", {"reviews_with_books": reviews_with_books}
    )


def index(request):
    # if request.method == 'POST':
    #     # Check if the form submission is for leaving a review
    #     form = ReviewForm(request.POST)
    #     if form.is_valid():
    #         # Process the review form submission
    #         book_id = form.cleaned_data['book_id']
    #         book = get_object_or_404(Book, id=book_id)
    #         review = form.save(commit=False)
    #         review.book = book
    #         review.user = request.user
    #         review.save()
    #         messages.success(request, 'Your review has been submitted successfully.')
    #         return redirect('index')  # Redirect back to the index page after review submission
    # else:
    google_book_api = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": "subject:science fiction|classic|crime and mystery|fantasy|true crime|Fiction",
        # "q": "subject: fiction",
        "maxResults": 40,
        # "fields": "items(id,volumeInfo/title,volumeInfo/authors,volumeInfo/imageLinks,volumeInfo/categories,volumeInfo/description)",
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


# @login_required
def book_detail(request, book_id):
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
    return render(request, "book_detail.html", {"book": book_data, "reviews": book_data["reviews"], 'comment_form': comment_form })


# @login_required
def leave_review(request, book_id):
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

    # Save book information in the BookInfo model
    book_info, created = BookInfo.objects.get_or_create(book_id=book_data["id"])
    book_info.book_title = book_data["title"]  # Update book title
    book_info.save()

    if not request.user.is_authenticated:
        login_url = reverse("login")
        login_link = f'<a class="login-link" href="{login_url}">Log in</a>'
        register_link = f'<a class="register-link" href="{reverse("register")}">Register</a>'
        messages.info(
            request,
            f"You need to log in to leave a review. Please {login_link} or {register_link}.",
        )
        return redirect("login")

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book_id = book_data["id"]
            review.book_title = book_data["title"]  # Associate book title with review
            review.book_author = book_data["author"]
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been submitted successfully.")
            return redirect("book_detail", book_id=book_id)
    else:
        form = ReviewForm()

    if not request.user.is_authenticated:
        messages.info(request, "You need to log in to leave a review.")

    return render(request, "leave_review.html", {"form": form, "book": book_data})






@login_required
def add_comment_to_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id) 
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.review = (
                review  
            )
            comment.save()
            messages.success(request, "Your comment has been added successfully.")
    return redirect("book_detail", book_id=review.book_id)


def search_books(request):
    form = SearchForm(request.GET)
    books = []

    if form.is_valid():
        query = form.cleaned_data["query"]
        category = form.cleaned_data.get(
            "category"
        )  

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
