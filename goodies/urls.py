from django.urls import path
from . import views

urlpatterns = [
    path('', views.goodies, name='goodies'),
    path('cart/<int:id>', views.cart, name='cart'),
    path('place/<int:id>',views.place,name='place-goodie'),
    path('tag/<str:tag>', views.category_goodies, name='tag-goodies'),
]
