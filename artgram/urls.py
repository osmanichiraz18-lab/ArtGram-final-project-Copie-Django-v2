from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from users.views import landing_page_view, login_view, register_view, logout_view, profile_complete_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page_view, name='landing'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('explore/', include('explore.urls')),
    path('artworks/', include('artworks.urls')),
    path('notifications/', include('notifications.urls')),
    path('profile/', include('users.profile_urls')),
    path('complete-profile/', profile_complete_view, name='profile_complete'),
    
    # Old URL redirects for backward compatibility
    path('users/login/', RedirectView.as_view(url='/login/', permanent=True), name='old_login'),
    path('users/register/', RedirectView.as_view(url='/register/', permanent=True), name='old_register'),
    path('users/logout/', RedirectView.as_view(url='/logout/', permanent=True), name='old_logout'),
    path('users/profile/<str:username>/', RedirectView.as_view(url='/profile/@%(username)s/', permanent=True), name='old_profile'),
    path('users/profile/edit/', RedirectView.as_view(url='/profile/@request.user.username/edit/', permanent=True), name='old_edit_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)