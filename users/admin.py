from django.contrib import admin
from .models import (Profile, Pomodoro, Badge, Reward, House, Teams)
from django.utils.html import format_html


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "batch", "phone")


@admin.register(Pomodoro)
class PomodoroAdmin(admin.ModelAdmin):
    list_display = ("user", "count", "energy", "productivity")


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("title", "points", "description")


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):

    @staticmethod
    def badge_photo(obj):
        return format_html('<img src="{}" width="40"  class="rounded-corners"/> <span>{}</span>'.format(obj.badges.logo.url, obj.badges.title))

    @staticmethod
    def user_photo(object):
        return format_html(
            '<img src="{}" width="40" height="40"/>'.format(object.user.profile.image.url))

    list_display = ("id", "user_photo", "user", "awarded_by", "badge_photo", "badges", "timestamp", "description")
    list_display_links = ("id", "user_photo", "user")
    search_fields = ("awarded_by", "user__username")
    list_filter = ("badges",)


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    pass


@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    pass
