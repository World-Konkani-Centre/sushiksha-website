from django.urls import path
from . import views

urlpatterns = [
    path('badge-claim/', views.badge_claim, name='badge_claim'),
    path('badge-claim/<int:pk>/', views.badge_claim_form, name='badge_claim_form'),

]
