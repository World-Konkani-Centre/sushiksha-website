from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name='coding-index'),
   path('compile/', views.compileCode, name='compile'),
   path('run/', views.runCode, name='run'),
]
