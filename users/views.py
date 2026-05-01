from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .form import UserRegistrationForm, UserProfileForm
from django.contrib import messages

def landing_page_view(request):
    """Landing page for unauthenticated users"""
    if request.user.is_authenticated:
        return redirect('explore:home')
    return render(request, 'landing.html')

def register_view(request):
    """Two-step registration view - Step 1: Basic account creation"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create user but don't save profile fields yet
            user = form.save(commit=False)
            user.bio = ""  # Set empty bio for now
            user.profile_picture = None  # Set empty profile picture for now
            user.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Let\'s complete your profile.')
            return redirect('profile_complete')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_complete_view(request):
    """Step 2: Profile completion after registration"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile completed! Welcome to ArtGram!')
            return redirect('explore:home')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/profile_complete.html', {'form': form})

def login_view(request):
    """Enhanced login view"""
    if request.method == 'POST':
        from django.contrib.auth import authenticate
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Try authentication with username first
        user = authenticate(request, username=username, password=password)
        
        # If that fails, try to find user by email and authenticate with username
        if user is None:
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        
        if user is not None:
            from django.contrib.auth import login
            login(request, user)
            return redirect('explore')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'users/login.html')

@login_required
def add_work_view(request):
    """Add new artwork view"""
    if request.method == 'POST':
        from artworks.models import Artwork
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        image = request.FILES.get('image')
        
        if title and image:
            artwork = Artwork.objects.create(
                artist=request.user,
                title=title,
                description=description,
                image=image
            )
            messages.success(request, 'Artwork uploaded successfully!')
            return redirect('profile:profile', username=request.user.username)
        else:
            messages.error(request, 'Please provide a title and image for your artwork.')
    
    return render(request, 'users/add_work.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request, username):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('explore')
    
    # Get user's artworks
    from artworks.models import Artwork
    artworks = Artwork.objects.filter(artist=profile_user).order_by('-created_at')
    
    # Check if current user is following this profile user
    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = request.user.is_following(profile_user)
    
    return render(request, 'users/profile.html', {
        'username': username,
        'profile_user': profile_user,
        'artworks': artworks,
        'is_following': is_following
    })

@login_required
def follow_user(request, username):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    try:
        user_to_follow = User.objects.get(username=username)
        if request.user == user_to_follow:
            messages.error(request, "You cannot follow yourself.")
        else:
            from .models import Follow
            Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
            messages.success(request, f"You are now following {user_to_follow.display_name or user_to_follow.username}!")
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
    
    return redirect('profile:profile', username=username)

@login_required
def unfollow_user(request, username):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    try:
        user_to_unfollow = User.objects.get(username=username)
        from .models import Follow
        follow = Follow.objects.filter(follower=request.user, following=user_to_unfollow).first()
        if follow:
            follow.delete()
            messages.success(request, f"You have unfollowed {user_to_unfollow.display_name or user_to_unfollow.username}.")
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
    
    return redirect('profile:profile', username=username)

@login_required
def edit_profile_view(request, username):
    """Edit profile view - only allow users to edit their own profile"""
    if request.user.username != username:
        messages.error(request, "You can only edit your own profile.")
        return redirect('profile:profile', username=request.user.username)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile:profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'users/edit_profile.html', {'form': form})
