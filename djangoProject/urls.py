from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import index, about, house, team

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('house/<int:id>', house, name='house'),
    path('team/<int:id>', team, name='team'),
    path('grappelli/', include('grappelli.urls')),
    path('logout/', auth_views.LogoutView.as_view(template_name='index.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('', index, name='home'),
    path('user/', include('users.urls')),
    path('', include('contact.urls')),
    path('blog/', include('blog.urls')),
    path('about/', about, name='about'),
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
