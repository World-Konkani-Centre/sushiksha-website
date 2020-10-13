from django.contrib import admin
from .models import Contact, Events, Testimonial, Faq


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "timestamp")


@admin.register(Events)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("title", "content", "date_and_time")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role")


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ("short_title", "question")

