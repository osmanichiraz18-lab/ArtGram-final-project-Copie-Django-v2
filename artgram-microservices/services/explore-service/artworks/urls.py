from django.urls import path
from . import views

app_name = 'artworks'

urlpatterns = [
    path('', views.artworks_home, name='home'),
    path('artwork/<slug:slug>/', views.artwork_detail, name='detail'),
    path('my-artworks/', views.my_artworks, name='my_artworks'),
    path('create/', views.create_artwork, name='create'),
    path('edit/<slug:slug>/', views.edit_artwork, name='edit'),
    path('delete/<slug:slug>/', views.delete_artwork, name='delete'),
]
