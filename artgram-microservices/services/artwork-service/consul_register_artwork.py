import consul
import os
import time
import threading

def register_service():
    """Register service with Consul"""
    try:
        consul_host = os.environ.get('CONSUL_HOST', 'localhost')
        consul_port = int(os.environ.get('CONSUL_PORT', '8500'))
        service_name = os.environ.get('SERVICE_NAME', 'artwork-service')
        service_port = int(os.environ.get('PORT', '8002'))
        service_id = f"{service_name}-{os.environ.get('HOSTNAME', 'local')}"
        
        print(f"Registering {service_name} with Consul...")
        
        # Wait for Consul to be available
        for i in range(30):
            try:
                c = consul.Consul(host=consul_host, port=consul_port)
                c.agent.self()
                print(f"Consul connected at {consul_host}:{consul_port}")
                break
            except Exception:
                if i == 29:
                    print(f"Consul not available after 30 seconds, continuing anyway...")
                    break
                time.sleep(1)
        
        # Register service
        c.agent.service.register(
            name=service_name,
            service_id=service_id,
            port=service_port,
            tags=['artgram', 'microservice', 'artwork'],
            check=consul.Check.http(f"http://{service_name}:{service_port}/health/", interval="10s")
        )
        
        print(f"✅ {service_name} registered with Consul!")
        print(f"   Service ID: {service_id}")
        print(f"   Health Check: http://{service_name}:{service_port}/health/")
        
        # Keep service registration alive
        while True:
            time.sleep(30)
            
    except Exception as e:
        print(f"❌ Consul registration failed: {e}")

if __name__ == "__main__":
    register_service()
