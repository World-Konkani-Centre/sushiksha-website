from django.contrib import admin
from csvexport.actions import csvexport
from .models import (Profile, Pomodoro, Badge, Reward, House, Teams, BadgeCategory, Mentions)
from django.utils.html import format_html, escape
from django.contrib.admin.models import LogEntry, DELETION
from django.urls import reverse
from django.utils.safestring import mark_safe


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "role", "batch", "phone", "name", "college", "points")
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
    search_fields = ("title", "category__name")
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
    filter_horizontal = ('teams', )
    actions = [csvexport]


@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    filter_horizontal = ('members', )
    actions = [csvexport]


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"