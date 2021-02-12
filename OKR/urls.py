from django.conf.urls import url
from . import views

urlpatterns = [
    url('ajax/load-entry/', views.load_okr, name="ajax-load"),
    url('', views.view_data, name="okr-view-data"),
]
