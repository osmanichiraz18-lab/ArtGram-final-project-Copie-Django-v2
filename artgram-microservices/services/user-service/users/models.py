from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    display_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nom affiché')
    bio = models.TextField(blank=True, null=True, verbose_name='Biographie')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name='Photo de profil')
    is_artist = models.BooleanField(default=True, verbose_name='Artiste')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    
    def __str__(self):
        return self.username
    
    def get_artworks_count(self):
        return self.artworks.count()
    
    def get_likes_received_count(self):
        total = 0
        for artwork in self.artworks.all():
            total += artwork.likes.count()
        return total
    
    def get_followers_count(self):
        return self.followers.count()
    
    def get_following_count(self):
        return self.following.count()
    
    def is_following(self, user):
        return self.following.filter(following=user).exists()
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
    
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"