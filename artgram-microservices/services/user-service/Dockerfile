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
EXPOSE 8001

# Copy startup script
COPY start.sh .
RUN chmod +x start.sh

# Run the startup script
CMD ./start.sh
