from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('permissions/', views.user_permissions_view, name='permissions'),
    path('roles/', views.RoleManagementView.as_view(), name='roles'),
    path('assign-role/', views.assign_role_view, name='assign_role'),
]
