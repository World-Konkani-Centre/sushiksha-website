from django.conf.urls import url
from . import views

urlpatterns = [
    url('', views.view_data, name="okr-view-data"),
    url('<int:id>/', views.load_okr, name="okr-view-id"),
]
