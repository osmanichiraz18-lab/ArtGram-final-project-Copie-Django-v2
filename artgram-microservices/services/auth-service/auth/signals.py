from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Role

@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    """Create default roles after migration"""
    if sender.name == 'auth':
        Role.objects.get_or_create(
            name='admin',
            defaults={
                'description': 'Administrator with full access',
                'permissions': {
                    'permissions': ['create', 'read', 'update', 'delete', 'manage_users', 'manage_roles']
                }
            }
        )
        
        Role.objects.get_or_create(
            name='artist',
            defaults={
                'description': 'Artist who can create and manage their own artworks',
                'permissions': {
                    'permissions': ['create_artwork', 'read_artwork', 'update_own_artwork', 'delete_own_artwork']
                }
            }
        )
        
        Role.objects.get_or_create(
            name='user',
            defaults={
                'description': 'Regular user with basic permissions',
                'permissions': {
                    'permissions': ['read_artwork', 'like_artwork', 'comment_artwork']
                }
            }
        )
