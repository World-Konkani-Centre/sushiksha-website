from django.urls import path
from . import views

urlpatterns = [
    path('', views.goodies, name='goodies'),
]
