from django.conf.urls import url
from . import views

urlpatterns = [
    url('objectives/', views.create_objectives, name="create-objectives"),
    url('key-result/', views.create_key_results, name="create-key-result"),
    url('entry/', views.insert_data, name="okr-insert-entry"),
    url('ajax/load-entry/', views.load_okr, name="ajax-load"),
    url('', views.view_data, name="okr-view-data"),
]
