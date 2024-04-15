from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Review, Commenting
# from .models import BookInfo

# Register your models here.
admin.site.register(CustomUser, UserAdmin)
# admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Commenting)
# admin.site.register(BookInfo)