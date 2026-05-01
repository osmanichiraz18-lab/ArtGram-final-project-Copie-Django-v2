from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('@<str:username>/', views.profile_view, name='profile'),
    path('@<str:username>/edit/', views.edit_profile_view, name='edit_profile'),
    path('add-work/', views.add_work_view, name='add_work'),
    path('health/', views.health_check, name='health'),
]