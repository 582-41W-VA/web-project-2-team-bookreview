from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from tweet.models import CustomUser, Tweet, Follow
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import requests


@login_required
def index(request):
    """test request localhost:8000 get for homepage will return hello world from homepage"""
    user_login = request.user.id

    if user_login:

        user_info = CustomUser.objects.get(id=user_login)
        user_following = Follow.objects.filter(follower=user_login)

        user_following_id_list = user_following.values_list("following__id", flat=True)
        user_follower = Follow.objects.filter(following=user_login)

        user_login_combine_following = list(user_following_id_list) + [user_login]
        tweets_from_following = Tweet.objects.filter(
            user__id__in=user_login_combine_following
        ).order_by("-created_at")

        context = {
            "following": user_following,
            "followers": user_follower,
            "tweets": tweets_from_following,
            "user": user_info,
        }

        return render(request, "tweet/index.html", context)

    return HttpResponseRedirect(reverse("login"))


def error_response(request, msg):

    context = {"message": msg}
    return render(request, "tweet/404.html", context)


def register(request):
    if request.method == "POST":
        try:
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]

            hashed_password = make_password(password)

            user_register = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=hashed_password,
            )
            user_register.save()

            return HttpResponseRedirect(reverse("login"))

        except KeyError:
            error_response(request, "Missing Information, Cannot register")

    return render(request, "tweet/register.html")


def user_login(request):
    if request.method == "POST":
        try:
            username = request.POST["username"]
            password = request.POST["password"]

            user_login = authenticate(request, username=username, password=password)
            if user_login:
                login(request, user_login)

                return HttpResponseRedirect(reverse("home"))
        except KeyError:
            error_response(request, "Data does not match, Cannot Login")

    return render(request, "tweet/login.html")


def user_logout(request):

    logout(request)

    return HttpResponseRedirect(reverse("login"))


@login_required
def tweet(request):
    user_id = request.user.id
    login_user = CustomUser.objects.get(id=user_id)

    if request.method == "POST":
        try:
            user_tweet = request.POST["tweet"]
            user = login_user

            add_tweet = Tweet(user=user, content=user_tweet)

            add_tweet.save()

        except KeyError:
            error_response(request, "Cannot Tweet")

        return HttpResponseRedirect(reverse("home"))


@login_required
def user_profile(request, username):

    profile = CustomUser.objects.get(username=username)
    login_user = request.user

    is_following = Follow.objects.filter(
        follower=login_user, following=profile
    ).exists()

    if profile:
        if is_following:

            context = {"user_info": profile, "btn": "Unfollow"}
            return render(request, "tweet/profile.html", context)

        context = {"user_info": profile, "btn": "Follow"}
        return render(request, "tweet/profile.html", context)

    context = {"message": "User Not Found"}
    return render(request, "tweet/profile.html", context)


@login_required
def search_user(request):
    if request.method == "POST":
        username = request.POST["username"]

        users = CustomUser.objects.filter(username__icontains=username)
        context = {"users": users}
        return render(request, "tweet/search_user.html", context)

    return render(request, "tweet/search_user.html")


@login_required
def follow_user(request, following_id):
    login_user = request.user
    following_user = get_object_or_404(CustomUser, id=following_id)

    # Check if the user is already following the target user
    is_following = Follow.objects.filter(
        follower=login_user, following=following_user
    ).exists()

    if is_following:
        # If already following, unfollow
        Follow.objects.filter(follower=login_user, following=following_user).delete()
        message = f"You have unfollowed {following_user.username}."
        btn = "Follow"

    else:
        # If not following, follow
        follow_instance = Follow(follower=login_user, following=following_user)
        follow_instance.save()
        message = f"Now you are following {following_user.username}."
        btn = "Unfollow"

    context = {
        "message": message,
        "user_info": following_user,
        "isFollow": is_following,
        "btn": btn,
    }

    return render(request, "tweet/profile.html", context)


def api_call(request):

    google_book_api = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": "subject:science fiction|classic|crime and mystery",
        "maxResults": 40,
        "fields": "items(id,volumeInfo/title,volumeInfo/authors,volumeInfo/imageLinks,volumeInfo/categories,volumeInfo/description)",
    }

    response = requests.get(google_book_api, params=params).json()

    sorted_data = []

    for data in response["items"]:
        info = data["volumeInfo"]
        new_data = {
            "id": data["id"],
            "title": info["title"],
            "author": info.get("authors", ["Author Not Available"])[0],
            "description": info.get("description", "No Description"),
            "category": info.get(
                "categories",
                "No Categories",
            )[0],
            "image": info.get("imageLinks", {}).get(
                "thumbnail", "https://islandpress.org/files/default_book_cover_2015.jpg"
            ),
        }

        sorted_data.append(new_data)

    context = {"books": sorted_data}

    return render(request, "tweet/book.html", context)

    # if want implement with function inside your function
    return sorted_data

    # return JsonResponse(list(sorted_data), safe=False)
