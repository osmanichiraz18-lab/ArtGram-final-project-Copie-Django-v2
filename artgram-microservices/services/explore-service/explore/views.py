from django.shortcuts import render
from artworks.models import Artwork

def explore_home(request):
    artworks = Artwork.objects.all().order_by('-created_at')
    return render(request, 'explore/home.html', {'artworks': artworks})
