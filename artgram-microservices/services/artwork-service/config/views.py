from django.http import JsonResponse


def health_check(request):
    """Health check endpoint for Consul"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'artwork-service',
        'version': '1.0.0'
    })
