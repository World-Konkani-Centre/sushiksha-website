from django.urls import path

from . import views

handler404 = 'djangoProject.views.handler404'
handler500 = 'djangoProject.views.handler500'
handler400 = 'djangoProject.views.handler400'
handler403 = 'djangoProject.views.handler403'

urlpatterns = [
    path('timer', views.timer, name='timer')
]

