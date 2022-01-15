from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('pentathlon/', views.pentathlon, name='pentathlon'),
    path('sessions/', views.sessions, name='sessions'),
    path('poll/', views.poll, name='poll'),
    path('poll/vote/<int:id>/<int:passw>/', views.vote, name='vote'),
    path('poll/auth/<int:id>/', views.votepass, name='auth-vote'),
    path('work-from-wkc/', views.work_from_wkc, name='work-from-wkc'),
    path('archive/', views.archive, name='archive')
]
