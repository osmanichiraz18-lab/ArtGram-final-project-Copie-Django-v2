from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('@<str:username>/', views.profile_view, name='profile'),
    path('@<str:username>/edit/', views.edit_profile_view, name='edit_profile'),
    path('@<str:username>/follow/', views.follow_user, name='follow'),
    path('@<str:username>/unfollow/', views.unfollow_user, name='unfollow'),
    path('add-work/', views.add_work_view, name='add_work'),
]
