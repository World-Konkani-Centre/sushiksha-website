from django.urls import path
from . import views
from badge.views import badge_list

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('', views.profile, name='profile'),
    # path('analytics/', views.log_pomodoro, name='analytics'),
    path('leaderboard/', views.leader, name='leaderboard'),
    path('members/', views.user_list_view, name='trainers'),
    path('search/', views.search, name='user-search'),
    path('badge/<int:id>/', views.create_badge, name='new-badge'),
    path('badge/', views.badge, name='badge'),
    path('multiple-badge/', views.multi_badge, name='multiple-badge'),
    path('rewards/', badge_list, name='reward'),
    path('<int:pk>/', views.user_detail_view, name='user-detail'),
    path('logs/',views.get_logs , name='logs'),
    path('logs/profiles',views.get_profile_file , name='logs-profile'),
    path('logs/team/',views.get_team_file , name='logs-team'),
    path('logs/user/',views.get_user_file,name='logs-user'),
    path('logs/teams/', views.get_team_file_large, name='logs-teams'),
    path('logs/users/', views.get_user_file_large, name='logs-users'),
    path('logs/selecteduser/', views.get_single_user_file_large, name='logs-user-selected'),
    path('badge/slack/',views.slack_badge,name="slack-badge"),
    path('logs/okr/', views.okr_weekly, name="okr-weekly"),

    # path('delete/rewards', views.delete_rewards, name='delete'),
    # Deleting rewards for quarter
]
