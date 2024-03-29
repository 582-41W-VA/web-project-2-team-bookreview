from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from .managers import CustomUserManager
from django.core.validators import MaxValueValidator, MinValueValidator 

class CustomUser(AbstractUser):
    # Add custom fields as needed
    email = models.EmailField(unique=True)
    objects = CustomUserManager()
    class Meta:
            permissions = [
                ("can_view_users", "Can view users"),
                ("can_edit_users", "Can edit users"),
                ("can_delete_users", "Can delete users"),
                ("can_edit_reviews", "Can edit reviews"),
                ("can_delete_reviews", "Can delete reviews"),
                ("can_view_all_reviews", "Can view all reviews"),
                ("can_delete_comments", "Can delete comments"),
            ]

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
    review_date = models.DateTimeField(auto_now_add=True)

    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_content = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s review of {BookInfo.objects.get(book_id=self.book_id).book_title}"
    


class Commenting(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    comment_text = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s comment on {BookInfo.objects.get(book_id=self.review.book_id).book_title}"


# class AddComment(models.Model):
#     full_name = models.CharField(max_length=200)
#     age = models.PositiveIntegerField()
#     comment_text = models.TextField()
#     article = models.ForeignKey(Article, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Comment by {self.full_name} on {self.article.article_title}"


    

class BookInfo(models.Model):
    book_id = models.CharField(max_length=100, unique=True)
    book_title = models.CharField(max_length=255)

    def __str__(self):
        return self.book_title
    


# class Meta:
#     permissions = [
#         ("can_view_users", "Can view users"),
#         ("can_edit_users", "Can edit users"),
#     ]