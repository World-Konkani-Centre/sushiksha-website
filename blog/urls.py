from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('search/', views.search, name='search'),
    path('categories/<str:category>',views.categories_view,name='category'),
    path('post/<id>', views.blog_single, name='blog-detail'),
    path('post/', views.blog_create, name='blog-create'),
    path('post/<id>/update', views.blog_update, name='blog-update'),
    path('post/<id>/delete', views.blog_delete, name='blog-delete'),
    path('post/author/<id>/', views.user_post, name='user-posts'),
]
