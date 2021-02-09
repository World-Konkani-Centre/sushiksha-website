from django.urls import path
from . import views

urlpatterns = [
    # path('donut/', views.donut_form, name='donut_badge_claim'),
    # path('1:1/', views.one_one, name='one_one_badge_claim'),
    # path('book_reading/', views.book_reading, name='book_reading_claim'),
    # path('kt_attendee_feedback/', views.kt_attendee, name='kt_attendee_claim'),
    # path('kt_giver/', views.kt_giver, name='kt_giver_claim'),
    # # path('kt_session/', views.kt_session, name='kt_session_claim'),
    # path('initiator/', views.intiator, name='initiator_claim'),
    # path('blogger/', views.blog, name='blogger_claim')
    path('badge-claim/', views.badge_claim, name='badge_claim'),
    path('badge-claim/<int:pk>/', views.badge_claim_form, name='badge_claim_form'),

]
