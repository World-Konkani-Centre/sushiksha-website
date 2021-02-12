from django.conf.urls import url
from . import views

urlpatterns = [
    url('create-objectives/', views.create_objectives, name="create-objectives"),
    url('create-key-result/', views.create_key_results, name="create-key-result"),
    url('insert-entry/', views.insert_data, name="okr-insert-entry"),
    url('ajax/load-entry/', views.load_okr, name="ajax-load"),
    url('', views.view_data, name="okr-view-data"),

]
