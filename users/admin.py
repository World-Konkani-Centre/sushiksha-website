from django.contrib import admin
from csvexport.actions import csvexport
from .models import (Profile, Pomodoro, Badge, Reward, House, Teams, BadgeCategory, Mentions)
from django.utils.html import format_html


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "role", "batch", "phone", "name", "college", "points", "stars")
    search_fields = ("user__username", "role", "batch")
    list_filter = ("role", "batch")
    list_display_links = ("user", "id")
    actions = [csvexport]


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):

    @staticmethod
    def badge_photo(obj):
        return format_html('<img src="{}" width="50" /> <span>{}</span>'.format(obj.logo.url, obj.title))

    list_display = ("id", "badge_photo", "category", "featured", "title", "points", "description")
    list_display_links = ("id", "title")
    list_filter = ("points", "featured")
    search_fields = ("title", "category")
    list_editable = ("featured", "points", "description", "category")
    actions = [csvexport]


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):

    @staticmethod
    def badge_photo(obj):
        return format_html(
            '<img src="{}" width="40"  class="rounded-corners"/> <span>{}</span>'.format(obj.badges.logo.url,
                                                                                         obj.badges.title))

    @staticmethod
    def user_photo(object):
        return format_html(
            '<img src="{}" width="40" height="40"/>'.format(object.user.profile.image.url))

    list_display = ("id", "user_photo", "user", "awarded_by", "badge_photo", "badges", "timestamp", "description")
    list_display_links = ("id", "user_photo", "user")
    search_fields = ("awarded_by", "user__username")
    list_filter = ("badges",)
    actions = [csvexport]


@admin.register(BadgeCategory)
class BadgeCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    list_filter = ("id", "name")
    search_fields = ("name",)
    actions = [csvexport]


@admin.register(Mentions)
class MentionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "team", "house", "user")
    list_display_links = ("id", "title", "house", "user")
    search_fields = ("title",)
    actions = [csvexport]


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    actions = [csvexport]


@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    actions = [csvexport]
