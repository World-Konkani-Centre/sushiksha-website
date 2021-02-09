from django.contrib import admin
from .models import BadgeClaim


@admin.register(BadgeClaim)
class BadgeClaimAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')