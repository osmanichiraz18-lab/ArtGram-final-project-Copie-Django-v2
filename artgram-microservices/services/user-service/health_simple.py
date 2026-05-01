from django.http import JsonResponse

def health(request):
    """Health check endpoint for Consul"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'user-service',
        'version': '1.0.0'
    })
