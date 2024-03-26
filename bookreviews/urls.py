from django.urls import path
from . import views
from .views import my_reviews

urlpatterns = [
    path("", views.index, name='index'),
    path('book/<str:book_id>/', views.book_detail, name='book_detail'),
    path('book/<str:book_id>/leave_review/', views.leave_review, name='leave_review'),

    path('edit/<str:review_id>/', views.edit_review, name='edit_review'),
    path('delete/<str:review_id>/', views.delete_review, name='delete_review'),
    
    path('my-reviews/', my_reviews, name='my_reviews'),
    
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
]
