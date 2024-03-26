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
    id = models.CharField(primary_key=True, max_length=100)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255)  # Add this field
    image = models.URLField()  # Add this field

    def __str__(self):
        return self.title

# class Review(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
#     comment = models.TextField()

#     def __str__(self):
#         return f"{self.user.username}'s review of {self.book.title}"


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # Book information fetched from external API
    book_id = models.CharField(max_length=100)  # Unique identifier from the external API
    book_title = models.CharField(max_length=255)
    book_author = models.CharField(max_length=255)
    book_description = models.TextField()
    book_category = models.CharField(max_length=255)
    book_image = models.URLField()

    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s review of {self.book_title}"
    


class Commenting(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    comment_text = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s comment on {self.review.book_title}"


# class AddComment(models.Model):
#     full_name = models.CharField(max_length=200)
#     age = models.PositiveIntegerField()
#     comment_text = models.TextField()
#     article = models.ForeignKey(Article, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Comment by {self.full_name} on {self.article.article_title}"


    

class BookInfo(models.Model):
    book_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title