# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Make start script executable
RUN chmod +x start.sh || true

# Expose port (Railway will use PORT env variable at runtime)
# We expose 8000 as default, but Railway will use the PORT env var
EXPOSE 8000

# Run the application
# Railway provides PORT environment variable
CMD ["./start.sh"]

