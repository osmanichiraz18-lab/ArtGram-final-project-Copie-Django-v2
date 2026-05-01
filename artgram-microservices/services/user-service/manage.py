#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Register with Consul if running server
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        # Setup Django first
        import django
        django.setup()
        
        # Register with Consul
        try:
            from consul_registration_fixed import register_service
            register_service()
            
        except Exception as e:
            print(f"Consul registration failed: {e}")
    
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
