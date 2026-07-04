FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .
COPY templates/ templates/
COPY static/ static/

# Set environment variables
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run with hypercorn (supports HTTP/2)
# For HTTP/2 support, use: hypercorn --bind 0.0.0.0:8000 --http2 app:app
# For testing without HTTP/2: gunicorn --bind 0.0.0.0:8000 app:app
CMD ["hypercorn", "--bind", "0.0.0.0:8000", "--http2", "app:app"]
