from django.contrib import admin
from .models import CustomUser, Review, Commenting

# Register your models here.
admin.site.register(CustomUser)
# admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Commenting)
# admin.site.register(BookInfo)