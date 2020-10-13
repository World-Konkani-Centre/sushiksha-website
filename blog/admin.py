from django.contrib import admin
from .models import Categories, Post, Comment


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    pass
