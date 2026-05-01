from flask import Flask, jsonify
import os
import consul
import time
import threading

app = Flask(__name__)

@app.route('/health')
def health_check():
    """Health check endpoint for Consul"""
    return jsonify({
        'status': 'healthy',
        'service': 'user-service',
        'version': '1.0.0'
    })

def register_with_consul():
    """Register service with Consul"""
    try:
        # Wait for Consul to be available
        consul_host = os.environ.get('CONSUL_HOST', 'localhost')
        consul_port = int(os.environ.get('CONSUL_PORT', '8500'))
        service_name = os.environ.get('SERVICE_NAME', 'user-service')
        service_port = int(os.environ.get('PORT', '8001'))
        service_id = f"{service_name}-{os.environ.get('HOSTNAME', 'local')}"
        
        print(f"Registering {service_name} with Consul...")
        
        # Wait for Consul
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
            tags=['artgram', 'microservice', 'authentication'],
            check=consul.Check.http(f"http://{service_name}:{service_port}/health", interval="10s")
        )
        
        print(f"✅ {service_name} registered with Consul!")
        print(f"   Service ID: {service_id}")
        print(f"   Health Check: http://{service_name}:{service_port}/health")
        
    except Exception as e:
        print(f"❌ Consul registration failed: {e}")

if __name__ == '__main__':
    # Start Consul registration in background
    threading.Thread(target=register_with_consul, daemon=True).start()
    
    # Run Flask app
    port = int(os.environ.get('PORT', '8001'))
    app.run(host='0.0.0.0', port=port, debug=False)
