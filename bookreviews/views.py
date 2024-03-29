from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import Book, Review
from .forms import ReviewForm
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.urls import reverse
from .models import Review
import requests
from .models import BookInfo
from .models import Commenting
from .models import CustomUser

from .forms import CommentForm
from .forms import SearchForm
from .forms import UserEditForm


from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache


@login_required
@permission_required('bookreviews.can_edit_reviews')
def edit_any_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'The review has been edited successfully.')
            return redirect('book_detail', book_id=review.book_id)  # Redirect to book detail page
    else:
        form = ReviewForm(instance=review)
    # Pass the book data along with the form
    book_data = {
        "id": review.book_id,
        "title": review.book_title,
        "author": review.book_author,
        "description": review.book_description,
        "category": review.book_category,
        "image": review.book_image,
    }
    return render(request, 'edit_review.html', {'form': form, 'book': book_data})


@login_required
@permission_required('bookreviews.can_delete_reviews')
def delete_any_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST' and request.POST.get('delete_any_review') == 'yes':
        book_id = review.book_id  # Store the book ID before deletion
        review.delete()
        messages.success(request, 'Your review has been deleted successfully.')
        return redirect('book_detail', book_id=book_id)  # Redirect to book detail page after deletion
    else:
        # Pass the review to the template
        return render(request, 'delete_any_review.html', {'review': review})



@login_required
@permission_required('bookreviews.can_delete_comments')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Commenting, pk=comment_id)
    book_id = comment.review.book_id
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'The comment has been deleted successfully.')
    return redirect('book_detail', book_id=book_id)







# @permission_required('bookreviews.can_edit_reviews')
# def edit_any_review(request, review_id):
#     review = get_object_or_404(Review, id=review_id)
#     if review.user == request.user:  # Check if the logged-in user owns the review
#         if request.method == 'POST':
#             form = ReviewForm(request.POST, instance=review)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, 'Your review has been edited successfully.')
#                 return redirect('book_detail', book_id=review.book_id)  # Redirect to book detail page
#         else:
#             form = ReviewForm(instance=review)
#         # Pass the book data along with the form
#         book_data = {
#             "id": review.book_id,
#             "title": review.book_title,
#             "author": review.book_author,
#             "description": review.book_description,
#             "category": review.book_category,
#             "image": review.book_image,
#         }
#         return render(request, 'edit_review.html', {'form': form, 'book': book_data})



@permission_required('bookreviews.can_view_users')
def list_users(request):
    if not request.user.has_perm('bookreviews.can_view_users'):
        pass    
    users = CustomUser.objects.all()
    total_users = CustomUser.objects.count()
    return render(request, 'list_users.html', {'users': users,'total_users': total_users})


@permission_required('bookreviews.can_edit_user')
def edit_user(request, user_id):
    if not request.user.has_perm('bookreviews.can_edit_user'):
        pass
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('list_users')  # Redirect to the list of users after editing
    else:
        form = UserEditForm(instance=user)
    return render(request, 'edit_user.html', {'form': form, 'user': user})


@login_required
@permission_required('bookreviews.can_delete_users')
def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, pk=user_id)
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('list_users')  # Redirect to the list of users after deleting
    else:
        user = get_object_or_404(CustomUser, pk=user_id)
        return render(request, 'delete_user_confirm.html', {'user': user})




@login_required
@permission_required('bookreviews.can_view_all_reviews')
def total_reviews(request):
    total_reviews = Review.objects.count()
    return render(request, 'total_reviews.html', {'total_reviews': total_reviews})






# def index(request):
#     books = Book.objects.all()
#     return render(request, 'index.html', {'books': books})


# def book_detail(request, book_id):
#     book = Book.objects.get(id=book_id)
#     reviews = Review.objects.filter(book=book)
#     return render(request, 'book_detail.html', {'book': book, 'reviews': reviews})


# @login_required
# def leave_review(request, book_id):
#     if not request.user.is_authenticated:
#         login_url = reverse('login')
#         login_link = f'<a class="login-link" href="{login_url}">Log in</a>'
#         register_link = f'<a class="register-link" href="{reverse("register")}">Register</a>'
#         messages.info(request, f'You need to log in to leave a review. Please {login_link} or {register_link}.')
#         return redirect('login')
#     else:
#         book = get_object_or_404(Book, id=book_id)
#         if request.method == 'POST':
#             form = ReviewForm(request.POST)
#             if form.is_valid():
#                 review = form.save(commit=False)
#                 review.book = book  # Assign the current book to the review
#                 review.user = request.user  # Assign the logged-in user to the review
#                 review.save()
#                 messages.success(request, 'Your review has been submitted successfully.')
#                 return redirect('book_detail', book_id=book.id)  # Redirect to the book detail page
#         else:
#             form = ReviewForm()
#         return render(request, 'leave_review.html', {'form': form, 'book': book})
    




# def edit_review(request, review_id):
#     review = get_object_or_404(Review, id=review_id)
#     if review.user == request.user:  # Check if the logged-in user owns the review
#         if request.method == 'POST':
#             form = ReviewForm(request.POST, instance=review)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, 'Your review has been edited successfully.')
#                 return redirect('book_detail', book_id=review.book.id)  # Redirect to user's reviews page
#         else:
#             form = ReviewForm(instance=review)
#         return render(request, 'edit_review.html', {'form': form, 'book': review.book})
#     else:
#         return HttpResponseForbidden("You are not authorized to edit this review.")




# def delete_review(request, review_id):
#     review = get_object_or_404(Review, id=review_id)
#     if review.user == request.user:  # Check if the logged-in user owns the review
#         if request.method == 'POST' and request.POST.get('confirm_delete'):
#             review.delete()
#             messages.success(request, 'Your review has been deleted successfully.')
#             return redirect('book_detail', book_id=review.book.id)  # Redirect to book detail page after deletion
#         else:
#             return render(request, 'confirm_delete_review.html', {'review': review})
#     else:
#         return HttpResponseForbidden("You are not authorized to delete this review.")



def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user == request.user:  # Check if the logged-in user owns the review
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your review has been edited successfully.')
                return redirect('book_detail', book_id=review.book_id)  # Redirect to book detail page
        else:
            form = ReviewForm(instance=review)
        # Pass the book data along with the form
        book_data = {
            "id": review.book_id,
            "title": review.book_title,
            "author": review.book_author,
            "description": review.book_description,
            "category": review.book_category,
            "image": review.book_image,
        }
        return render(request, 'edit_review.html', {'form': form, 'book': book_data})
    else:
        return HttpResponseForbidden("You are not authorized to edit this review.")


# def delete_review(request, review_id):
#     review = get_object_or_404(Review, id=review_id)
#     if review.user == request.user:  # Check if the logged-in user owns the review
#         if request.method == 'POST' and request.POST.get('confirm_delete'):
#             book_id = review.book_id  # Store the book ID before deletion
#             review.delete()
#             messages.success(request, 'Your review has been deleted successfully.')
#             return redirect('book_detail', book_id=book_id)  # Redirect to book detail page after deletion
#         else:
#             # Pass the review and relevant book data along to the template
#             book_data = {
#                 "id": review.book_id,
#                 "title": review.book_title,
#                 "author": review.book_author,
#                 "description": review.book_description,
#                 "category": review.book_category,
#                 "image": review.book_image,
#             }
#             return render(request, 'confirm_delete_review.html', {'review': review})
#     else:
#         return HttpResponseForbidden("You are not authorized to delete this review.")



def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user == request.user:  # Check if the logged-in user owns the review
        if request.method == 'POST' and request.POST.get('confirm_delete'):
            book_id = review.book_id  # Store the book ID before deletion
            review.delete()
            messages.success(request, 'Your review has been deleted successfully.')
            return redirect('book_detail', book_id=book_id)  # Redirect to book detail page after deletion
        else:
            # Pass the review to the template
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


# @login_required
# def my_reviews(request):
#     user_reviews = Review.objects.filter(user=request.user)
#     return render(request, 'my_reviews.html', {'user_reviews': user_reviews})


# @login_required
# def my_reviews(request):
#     user_reviews = Review.objects.filter(user=request.user)
#     reviews_with_books = []

#     # Iterate over each review to fetch the corresponding book data from the API
#     for review in user_reviews:
#         # Fetch book data from the API using the book ID stored in the review
#         google_book_api = f"https://www.googleapis.com/books/v1/volumes/{review.book_id}"
#         response = requests.get(google_book_api).json()

#         if "error" not in response:
#             info = response["volumeInfo"]
#             book_data = {
#                 "title": info.get("title", "Title Not Available"),
#                 "author": info.get("authors", ["Author Not Available"])[0],
#                 "description": info.get("description", "No Description"),
#                 "category": info.get("categories", ["No Categories"])[0],
#                 "image": info.get("imageLinks", {}).get("thumbnail", "https://islandpress.org/files/default_book_cover_2015.jpg"),
#             }

#             # Append the review along with the fetched book data to the list
#             reviews_with_books.append({'review': review, 'book': book_data})

#     return render(request, 'my_reviews.html', {'reviews_with_books': reviews_with_books})





# @login_required
# def my_reviews(request):
#     # Check if the reviews_with_books data is already cached
#     reviews_with_books = cache.get('user_reviews_with_books')
    
#     # If not cached, retrieve the data and cache it
#     if not reviews_with_books:
#         # Retrieve the user's reviews
#         user_reviews = Review.objects.filter(user=request.user)
#         # Fetch additional book data based on the book ID in each review
#         reviews_with_books = []
#         for review in user_reviews:
#             # Fetch book data from API or any other source based on review.book_id
#             book_data = {
#                 "title": "Book Title",
#                 "author": "Book Author",
#                 # Add other book data as needed
#             }
#             reviews_with_books.append({"review": review, "book": book_data})
        
#         # Cache the data for future requests
#         cache.set('user_reviews_with_books', reviews_with_books, timeout=10)  # Cache for 15 minutes

#     return render(request, 'my_reviews.html', {'reviews_with_books': reviews_with_books})




@login_required
def my_reviews(request):
    user_reviews = Review.objects.filter(user=request.user)
    reviews_with_books = []

    # Iterate over each review to fetch the corresponding book data
    for review in user_reviews:
        # Define a unique cache key for each book using its ID
        cache_key = f'book_data_{review.book_id}'

        # Check if the book data is already cached
        book_data = cache.get(cache_key)

        if not book_data:
            # Fetch book data from the API if not found in the cache
            google_book_api = f"https://www.googleapis.com/books/v1/volumes/{review.book_id}"
            response = requests.get(google_book_api).json()

            if "error" not in response:
                info = response["volumeInfo"]
                book_data = {
                    "title": info.get("title", "Title Not Available"),
                    "author": info.get("authors", ["Author Not Available"])[0],
                    "description": info.get("description", "No Description"),
                    "category": info.get("categories", ["No Categories"])[0],
                    "image": info.get("imageLinks", {}).get("thumbnail", "https://islandpress.org/files/default_book_cover_2015.jpg"),
                }

                # Cache the fetched book data with the specified cache key
                cache.set(cache_key, book_data, timeout=3600)  # Cache for 1 hour (adjust timeout as needed)
            else:
                # Handle case where book data retrieval failed
                book_data = None

        # Append the review along with the book data to the list
        reviews_with_books.append({'review': review, 'book': book_data})

    return render(request, 'my_reviews.html', {'reviews_with_books': reviews_with_books})






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
                "image": info.get("imageLinks", {}).get("thumbnail", "https://islandpress.org/files/default_book_cover_2015.jpg"),
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
        "image": info.get("imageLinks", {}).get("thumbnail", "https://islandpress.org/files/default_book_cover_2015.jpg"),
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
        "image": info.get("imageLinks", {}).get("thumbnail", "https://islandpress.org/files/default_book_cover_2015.jpg"),
    }

    # Save book information in the BookInfo model
    book_info, created = BookInfo.objects.get_or_create(book_id=book_data["id"])
    book_info.title = book_data["title"]
    book_info.save()


    if not request.user.is_authenticated:
        login_url = reverse('login')
        login_link = f'<a class="login-link" href="{login_url}">Log in</a>'
        register_link = f'<a class="register-link" href="{reverse("register")}">Register</a>'
        messages.info(request, f'You need to log in to leave a review. Please {login_link} or {register_link}.')
        return redirect('login')
    # Check if the request method is POST
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book_id = book_data["id"]
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully.')
            return redirect('book_detail', book_id=book_id)  # Redirect to the book detail page
    else:
        form = ReviewForm()

    # If the user is not authenticated, display a warning message
    if not request.user.is_authenticated:
        messages.info(request, 'You need to log in to leave a review.')

    return render(request, 'leave_review.html', {'form': form, 'book': book_data})



@login_required
def add_comment_to_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)  # Retrieve the review object
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.review = review  # Associate the comment with the retrieved review object
            comment.save()
            messages.success(request, 'Your comment has been added successfully.')
    return redirect('book_detail', book_id=review.book_id)



def search_books(request):
    form = SearchForm(request.GET)
    books = []

    if form.is_valid():
        query = form.cleaned_data['query']
        category = form.cleaned_data.get('category')  # Assuming you have a category field in your SearchForm

        # Construct the API query URL with the search query and category filter
        google_books_api = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=40"
        if category:
            google_books_api += f"&subject={category}"

        response = requests.get(google_books_api).json()

        if 'items' in response:
            books = response['items']

    return render(request, 'search_results.html', {'form': form, 'books': books})
