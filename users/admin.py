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

    def user_photo(self, object):
        return format_html('<img src="{}" width="40"/> <span>{}</span>'.format(object.user.profile.image.url, object.user))

    def badge_photo(self, object):
        return format_html('<img src="{}" width="40"/> <span>{}</span>'.format(object.badges.logo.url, object.badges.title))

    list_display = ("id", "user_photo", "awarded_by", "badge_photo", "timestamp", "description")
    list_display_links = ("id", "user_photo",)
    search_fields = ("user", "badges", "awarded_by")
    list_filter = ("badges",)


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    pass


@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    pass
