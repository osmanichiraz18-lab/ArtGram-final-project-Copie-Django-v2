from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Artwork
from .form import ArtworkForm

def artworks_home(request):
    artworks = Artwork.objects.all().order_by('-created_at')
    return render(request, 'artworks/home.html', {'artworks': artworks})

def artwork_detail(request, slug):
    artwork = get_object_or_404(Artwork, slug=slug)
    artwork.views_count += 1
    artwork.save()
    return render(request, 'artworks/detail.html', {'artwork': artwork})

@login_required
def my_artworks(request):
    artworks = Artwork.objects.filter(artist=request.user).order_by('-created_at')
    return render(request, 'artworks/my_artworks.html', {'artworks': artworks})

@login_required
def create_artwork(request):
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.artist = request.user
            artwork.save()
            messages.success(request, 'Votre œuvre a été créée avec succès!')
            return redirect('artworks:detail', slug=artwork.slug)
    else:
        form = ArtworkForm()
    return render(request, 'artworks/create.html', {'form': form})

@login_required
def edit_artwork(request, slug):
    artwork = get_object_or_404(Artwork, slug=slug, artist=request.user)
    
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES, instance=artwork)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre œuvre a été mise à jour avec succès!')
            return redirect('artworks:detail', slug=artwork.slug)
    else:
        form = ArtworkForm(instance=artwork)
    
    return render(request, 'artworks/edit.html', {'form': form, 'artwork': artwork})

@login_required
def delete_artwork(request, slug):
    artwork = get_object_or_404(Artwork, slug=slug, artist=request.user)
    
    if request.method == 'POST':
        artwork.delete()
        messages.success(request, 'Votre œuvre a été supprimée avec succès!')
        return redirect('artworks:my_artworks')
    
    return render(request, 'artworks/delete.html', {'artwork': artwork})
