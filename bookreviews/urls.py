from django.urls import path
from . import views
from .views import my_reviews

urlpatterns = [
    path("", views.index, name='index'),
    path('book/<str:book_id>/', views.book_detail, name='book_detail'),
    path('book/<str:book_id>/leave_review/', views.leave_review, name='leave_review'),

    path('review/<str:review_id>/', views.review_detail, name='review_detail'),    

    path('edit/<str:review_id>/', views.edit_review, name='edit_review'),
    path('delete/<str:review_id>/', views.delete_review, name='delete_review'),

    path('review/<str:review_id>/comment/', views.add_comment_to_review, name='add_comment_to_review'),    
    
    path('my-reviews/', my_reviews, name='my_reviews'),

    path('search/', views.search_books, name='search_books'),
    
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),


    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('list_users/', views.list_users, name='list_users'),
    path('edit_user/<str:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<str:user_id>/', views.delete_user, name='delete_user'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    
    path('edit_any_review/<str:review_id>/', views.edit_any_review, name='edit_any_review'),
    path('delete_any_review/<str:review_id>/', views.delete_any_review, name='delete_any_review'),
    
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    path('total_reviews/', views.total_reviews, name='total_reviews'),
    path('search_users_reviews/', views.search_users_reviews, name='search_users_reviews'),
]
