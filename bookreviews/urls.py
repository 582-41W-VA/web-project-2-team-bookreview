from django.urls import path
from . import views
from .views import my_reviews

urlpatterns = [
    path("", views.index, name='index'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),

    
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
]
