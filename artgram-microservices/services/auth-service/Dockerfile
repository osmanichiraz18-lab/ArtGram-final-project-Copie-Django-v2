FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create media directory for uploads
RUN mkdir -p media

# Expose port
EXPOSE 8006

# Run migrations and start the server
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8006
