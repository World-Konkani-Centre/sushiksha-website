from django.contrib import admin
from .models import Objective, KR, Entry
from django import forms


@admin.register(Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ('user', 'objective')
    list_filter = ('user',)
    search_fields = ('user', 'objective', 'objective__key_result')


@admin.register(KR)
class KRAdmin(admin.ModelAdmin):
    list_display = ( 'user','objective','key_result')
    list_filter = ('objective__user__profile__name', 'objective')
    search_fields = ('objective__user', 'objective', 'key_result')

    def user(self,obj):
        return obj.objective.user.profile.name
    user.admin_order_field = 'user'


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    def objective(self, obj):
        return obj.key_result.objective

    list_display = ('id', 'user', 'objective', 'key_result', 'date_time')
    list_filter = ('user',)
    list_display_links = ('id', 'user')
