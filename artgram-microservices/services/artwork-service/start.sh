#!/bin/bash

# Run migrations first
python manage.py migrate

# Start the server in background and register with Consul
python manage.py runserver 0.0.0.0:8002 &
SERVER_PID=$!

# Give the server a moment to start
sleep 3

# Wait a bit more for Consul to be ready
sleep 5

# Register with Consul
python -c "
import os
import sys
import time
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

# Wait for Consul to be available
import consul
consul_host = os.environ.get('CONSUL_HOST', 'consul')
consul_port = int(os.environ.get('CONSUL_PORT', '8500'))

for i in range(60):
    try:
        c = consul.Consul(host=consul_host, port=consul_port)
        c.agent.self()
        print(f'Consul connected at {consul_host}:{consul_port}')
        break
    except Exception:
        if i == 59:
            print(f'Consul not available after 60 seconds, continuing anyway...')
            break
        time.sleep(1)

try:
    from consul_registration import register_service
    register_service()
except Exception as e:
    print(f'Consul registration failed: {e}')
"

# Wait for the server process
wait $SERVER_PID
