from django.contrib import admin
from .models import (Profile, Pomodoro, Badge, Reward, House, Teams )


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
    list_display = ("user", "awarded_by", "decision", "timestamp")


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    pass


@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    pass
