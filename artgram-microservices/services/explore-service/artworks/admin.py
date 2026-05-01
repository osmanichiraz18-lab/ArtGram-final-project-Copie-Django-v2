from django.contrib import admin
from .models import Artwork

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'category', 'year', 'get_likes_count', 'created_at')
    list_filter = ('category', 'created_at', 'artist')
    search_fields = ('title', 'description', 'artist__username')
    prepopulated_fields = {'slug': ('title',)}