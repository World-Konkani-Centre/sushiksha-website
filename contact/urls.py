from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('pentathlon/', views.pentathlon, name='pentathlon'),
    path('sessions/', views.sessions, name='sessions')
    # path('gallery/', views.gallery, name='gallery')
]
