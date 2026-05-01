from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Artwork(models.Model):
    CATEGORY_CHOICES = (
        ('Painting', 'Peinture'),
        ('Photography', 'Photographie'),
        ('Digital', 'Art Digital'),
        ('Mixed', 'Technique Mixte'),
        ('Sculpture', 'Sculpture'),
        ('Drawing', 'Dessin'),
    )
    
    title = models.CharField(max_length=200, verbose_name='Titre')
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(verbose_name='Description')
    image = models.ImageField(upload_to='artworks/', verbose_name='Image')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Painting')
    artist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='artworks')
    year = models.IntegerField(null=True, blank=True, verbose_name='Année de création')
    medium = models.CharField(max_length=100, blank=True, verbose_name='Technique')
    views_count = models.IntegerField(default=0, verbose_name='Vues')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.id}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_likes_count(self):
        return self.likes.count()
    
    def get_comments_count(self):
        return self.comments.count()
    
    def get_shares_count(self):
        return self.shares.count()
    
    class Meta:
        verbose_name = 'Œuvre'
        verbose_name_plural = 'Œuvres'
        ordering = ['-created_at']