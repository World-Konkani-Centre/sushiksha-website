from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('pentathlon/', views.pentathlon, name='pentathlon'),
    # path('gallery/', views.gallery, name='gallery')
]
