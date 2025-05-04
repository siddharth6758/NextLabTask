from django.contrib import admin
from app_track.models import Category, SubCategory, Apps

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Apps)