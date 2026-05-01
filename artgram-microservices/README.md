# ArtGram Microservices Architecture

This is a complete microservices refactoring of the ArtGram Django application. Each service runs independently with its own database and communicates via REST API calls.

## 🏗️ Architecture Overview

```
artgram-microservices/
├── docker-compose.yml          # Orchestrates all services
├── nginx/
│   └── nginx.conf              # API Gateway configuration
├── services/
│   ├── user-service/           # User authentication & profiles (Port 8001)
│   ├── artwork-service/        # Artwork CRUD & uploads (Port 8002)
│   ├── explore-service/        # Gallery browsing (Port 8003)
│   ├── interaction-service/    # Likes, views, comments (Port 8004)
│   └── notification-service/   # User alerts (Port 8005)
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git (to clone the repository)

### Running the Application

1. **Navigate to the microservices directory:**
   ```bash
   cd artgram-microservices
   ```

2. **Start all services with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - **API Gateway**: http://localhost:8000
   - **Health Check**: http://localhost:8000/health

### Stopping the Application
```bash
docker-compose down
```

## 📁 Service Structure

Each service follows this structure:
```
service-name/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Container configuration
├── config/                      # Django configuration
│   ├── settings.py             # Service-specific settings
│   └── urls.py                 # Service URL routing
└── <app_name>/                 # Original Django app (untouched)
```

## 🔌 API Endpoints

### User Service (Port 8001)
- `GET /api/users/` - List all users
- `POST /api/users/register/` - Register new user
- `POST /api/users/login/` - User login
- `GET /api/users/profile/{username}/` - Get user profile

### Artwork Service (Port 8002)
- `GET /api/artworks/` - List all artworks
- `POST /api/artworks/create/` - Create new artwork
- `GET /api/artworks/{id}/` - Get artwork details
- `PUT /api/artworks/{id}/edit/` - Update artwork
- `DELETE /api/artworks/{id}/delete/` - Delete artwork

### Explore Service (Port 8003)
- `GET /api/explore/` - Browse gallery
- `GET /api/explore/featured/` - Get featured artworks

### Interaction Service (Port 8004)
- `POST /api/interactions/like/` - Like an artwork
- `POST /api/interactions/comment/` - Comment on artwork
- `GET /api/interactions/views/{id}/` - Get view count

### Notification Service (Port 8005)
- `GET /api/notifications/` - Get user notifications
- `POST /api/notifications/create/` - Create notification

## 🌐 API Gateway Routes

The Nginx API Gateway routes requests as follows:
- `/api/users/` → `user-service:8001`
- `/api/artworks/` → `artwork-service:8002`
- `/api/explore/` → `explore-service:8003`
- `/api/interactions/` → `interaction-service:8004`
- `/api/notifications/` → `notification-service:8005`

## 🔗 Inter-Service Communication

Services communicate using HTTP requests. Here's an example:

```python
# explore-service/explore/service_client.py
import requests

class ArtworkServiceClient:
    def __init__(self):
        self.base_url = "http://artwork-service:8002/api/artworks/"
    
    def get_all_artworks(self):
        try:
            response = requests.get(self.base_url)
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error calling artwork service: {e}")
            return None

# Usage in views
def explore_home(request):
    client = ArtworkServiceClient()
    artworks = client.get_all_artworks()
    return render(request, 'explore/home.html', {'artworks': artworks})
```

## 🗄️ Database Architecture

Each service has its own SQLite database:
- `user-service/db.sqlite3` - User data
- `artwork-service/db.sqlite3` - Artwork data
- `explore-service/db.sqlite3` - Browse data
- `interaction-service/db.sqlite3` - Interaction data
- `notification-service/db.sqlite3` - Notification data

## 🐳 Docker Configuration

### Dockerfile Template
Each service uses a similar Dockerfile:
```dockerfile
FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p media
EXPOSE <PORT>
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:<PORT>
```

### Docker Compose Services
Each service is defined with:
- Build context pointing to its folder
- Port mapping (8001-8005)
- Volume mounts for development
- Network configuration
- Dependencies on nginx

## 🔧 Configuration Files Explained

### nginx.conf
- **Purpose**: API Gateway that routes traffic to services
- **Upstreams**: Define service endpoints
- **Location blocks**: Route specific URL patterns to services
- **Proxy settings**: Forward headers and handle CORS

### settings.py (per service)
- **Purpose**: Django configuration for each service
- **Key settings**:
  - `INSTALLED_APPS`: Only includes necessary apps for that service
  - `DATABASES`: Separate SQLite database per service
  - `CORS_ALLOWED_ORIGINS`: Allows inter-service communication
  - `SERVICE_PORT`: Unique port for each service

### docker-compose.yml
- **Purpose**: Orchestrates all containers
- **Services**: Defines each microservice
- **Networks**: Creates communication bridge between services
- **Volumes**: Persists media files separately

## 🛠️ Development Workflow

### Adding a New Feature
1. Identify which service needs the feature
2. Modify the appropriate Django app in that service
3. Update inter-service communication if needed
4. Test via the API Gateway at localhost:8000

### Debugging
- Check service logs: `docker-compose logs <service-name>`
- Access individual service directly: `http://localhost:<port>`
- Test API endpoints directly: `curl http://localhost:8000/api/artworks/`

### Database Migrations
```bash
# Run migrations for a specific service
docker-compose exec <service-name> python manage.py migrate

# Create new migrations
docker-compose exec <service-name> python manage.py makemigrations
```

## 🔒 Security Considerations

- Each service has its own SECRET_KEY
- CORS is configured for inter-service communication
- Services communicate internally via Docker network
- External access only through API Gateway

## 📈 Scaling

To scale a service:
```yaml
# In docker-compose.yml
services:
  artwork-service:
    # ... existing config
    deploy:
      replicas: 3  # Scale to 3 instances
```

## 🐛 Troubleshooting

### Common Issues
1. **Port conflicts**: Ensure ports 8000-8005 are free
2. **Service communication**: Check Docker network connectivity
3. **Database issues**: Each service has its own database file
4. **CORS errors**: Verify CORS settings in service settings

### Health Check
```bash
curl http://localhost:8000/health
```

## 📚 Next Steps

This microservices architecture provides a solid foundation for:
- Adding more services (e.g., search, recommendations)
- Implementing message queues for async communication
- Adding API authentication and rate limiting
- Setting up monitoring and logging
- Deploying to production with container orchestration

## 🤝 Beginner Tips

1. **Start simple**: Focus on one service at a time
2. **Use the API Gateway**: Always access services through localhost:8000
3. **Check logs**: Use `docker-compose logs` to debug issues
4. **Test APIs**: Use tools like Postman or curl to test endpoints
5. **Understand the flow**: Trace requests from API Gateway to service and back
