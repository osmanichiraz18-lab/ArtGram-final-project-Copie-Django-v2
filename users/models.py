from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_artist = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
    
    def get_artworks_count(self):
        return self.artworks.count()
    
    def get_likes_received_count(self):
        total = 0
        for artwork in self.artworks.all():
            total += artwork.likes.count()
        return total