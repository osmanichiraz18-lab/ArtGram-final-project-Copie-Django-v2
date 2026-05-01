import consul
import os
import requests
import time
from django.conf import settings

def register_service():
    """Register this service with Consul"""
    if not settings.CONSUL_ENABLED:
        return
    
    try:
        c = consul.Consul(host=settings.CONSUL_HOST, port=settings.CONSUL_PORT)
        
        service_id = f"{settings.SERVICE_NAME}-{os.environ.get('HOSTNAME', 'local')}"
        
        # Register service
        c.agent.service.register(
            name=settings.SERVICE_NAME,
            service_id=service_id,
            port=settings.SERVICE_PORT,
            tags=['artgram', 'microservice'],
            check=consul.Check.http(f"http://{settings.SERVICE_NAME}:{settings.SERVICE_PORT}/api/health/", interval="10s")
        )
        
        print(f"Service {settings.SERVICE_NAME} registered with Consul")
        
    except Exception as e:
        print(f"Failed to register with Consul: {e}")

def deregister_service():
    """Deregister this service from Consul"""
    if not settings.CONSUL_ENABLED:
        return
    
    try:
        c = consul.Consul(host=settings.CONSUL_HOST, port=settings.CONSUL_PORT)
        
        service_id = f"{settings.SERVICE_NAME}-{os.environ.get('HOSTNAME', 'local')}"
        c.agent.service.deregister(service_id)
        
        print(f"Service {settings.SERVICE_NAME} deregistered from Consul")
        
    except Exception as e:
        print(f"Failed to deregister from Consul: {e}")

def wait_for_consul():
    """Wait for Consul to be available"""
    max_retries = 30
    retry_interval = 2
    
    for i in range(max_retries):
        try:
            c = consul.Consul(host=settings.CONSUL_HOST, port=settings.CONSUL_PORT)
            c.agent.self()
            print("Consul is available")
            return True
        except Exception:
            print(f"Waiting for Consul... ({i+1}/{max_retries})")
            time.sleep(retry_interval)
    
    print("Consul not available after retries")
    return False
