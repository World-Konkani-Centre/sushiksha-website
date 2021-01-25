from django.contrib import admin
from .models import Goodie


@admin.register(Goodie)
class GoodieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "tag", "description", "is_shown", "is_link", "is_image")
    search_fields = ("title", "tag", "description")
    list_filter = ("is_shown", "is_image", "is_link")
    list_editable = ("is_shown", "is_image", "is_link")
    list_display_links = ("title", "id", "tag")
