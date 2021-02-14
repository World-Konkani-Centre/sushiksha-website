from django.contrib import admin
from .models import Contact, Testimonial, OneOneSession


# Events, , Faq, Gallery


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "timestamp")


# @admin.register(Events)
# class ContactAdmin(admin.ModelAdmin):
#     list_display = ("title", "content", "date_and_time")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role")


@admin.register(OneOneSession)
class OneOneSessionAdmin(admin.ModelAdmin):
    list_display = ("heading", "color")
    list_display_links = ('heading', 'color')
#
#
# @admin.register(Gallery)
# class GalleryAdmin(admin.ModelAdmin):
#     list_display = ("name", "image", "user", "featured")
