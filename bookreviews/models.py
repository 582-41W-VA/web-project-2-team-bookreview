from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from .managers import CustomUserManager
from django.core.validators import MaxValueValidator, MinValueValidator


class CustomUser(AbstractUser):
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
            ("can_access_admin_panel", "Can access admin panel"),
            ("can_search_users_in_admin_panel", "Can search users in admin panel"),
            (
                "can_view_user_details_in_admin_panel",
                "Can view user details in admin panel",
            ),
            ("can_search_reviews_in_admin_panel", "Can search reviews in admin panel"),
        ]

    def __str__(self):
        return self.username


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

    rating = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_content = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s review of {self.book_title} | review ID {self.id}"


class Commenting(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    comment_text = models.TextField( max_length=100)

    def __str__(self):
        return f"{self.user.username}'s comment on {self.review}"

