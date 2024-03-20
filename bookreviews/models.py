from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from django.core.validators import MaxValueValidator, MinValueValidator 

class CustomUser(AbstractUser):
    # Add custom fields as needed
    email = models.EmailField(unique=True)

    # Use the custom manager
    objects = CustomUserManager()

    # Define additional properties or methods if necessary

    def __str__(self):
        return self.username

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s review of {self.book.title}"
