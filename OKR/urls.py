from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_data, name="okr-view-data"),
    path('entries/<int:pk>/', views.load_okr, name="okr-view-id"),
]
