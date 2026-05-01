from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_artist', 'is_staff', 'created_at')
    list_filter = ('is_artist', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    readonly_fields = ('created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('ArtGram Informations', {
            'fields': ('bio', 'profile_picture', 'is_artist', 'created_at'),
        }),
    )