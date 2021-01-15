from django.urls import path
from . import views

urlpatterns = [
    path('donut/', views.donut_form, name='donut_badge_claim'),
    path('one_one/', views.donut_form, name='one_one_badge_claim'),
    path('book_reading/', views.donut_form, name='book_reading_claim'),
    path('kt_attendee/', views.donut_form, name='kt_attendee_claim'),
    path('kt_giver/', views.donut_form, name='kt_giver_claim'),
    path('kt_session/', views.donut_form, name='kt_session_claim'),
    path('initiator/', views.donut_form, name='initiator_claim')
]
