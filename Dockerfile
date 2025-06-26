FROM python:3.13-slim

# Metadata labels
LABEL vendor="smartgic.io" \
      source="https://github.com/smartgic/shortgic" \
      authors="Gaëtan Trellu <gaetan.trellu@smartgic.io>" \
      title="ShortGic URL Shortener" \
      description="Lightning fast URL shortener using FastAPI, SQLAlchemy and SQLite" \
      version="1.0.0"

# Set environment variables for Python optimization
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/home/shortgic/.local/bin:$PATH"

# Install system dependencies and security updates
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        # Required for some Python packages
        gcc \
        libc6-dev && \
    # Clean up apt cache to reduce image size
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create non-root user for security
RUN groupadd -r -g 1000 shortgic && \
    useradd -r -u 1000 -g shortgic -d /home/shortgic -s /sbin/nologin shortgic && \
    mkdir -p /home/shortgic/.local/bin /app /data && \
    chown -R shortgic:shortgic /home/shortgic /app /data && \
    chmod 755 /data

# Switch to non-root user
USER shortgic

# Set working directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY --chown=shortgic:shortgic requirements.txt .

# Install Python dependencies
RUN pip install --user --no-cache-dir --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=shortgic:shortgic app/ ./app/

# Create volume mount point for database persistence
VOLUME ["/data"]

# Set default environment variables
ENV SHORTGIC_DATABASE_PATH="/data/shortgic.db"

# Expose port
EXPOSE 8000

# Health check for container orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

# Use exec form for better signal handling
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
