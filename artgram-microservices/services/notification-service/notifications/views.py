from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications_home(request):
    # Get only received notifications for the current user
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    
    # Mark notifications as read when viewed
    notifications.filter(is_read=False).update(is_read=True)
    
    context = {
        'notifications': notifications,
        'unread_count': Notification.objects.filter(recipient=request.user, is_read=False).count()
    }
    return render(request, 'notifications/home.html', context)
