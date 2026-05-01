from django.http import JsonResponse

def health_view(request):
    """Health check endpoint for Consul"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'user-service',
        'version': '1.0.0'
    })
