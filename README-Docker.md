# ShortGic Docker Deployment Guide

This guide explains how to deploy ShortGic using Docker and Docker Compose.

## Quick Start

### 1. Basic Deployment

```bash
# Clone the repository
git clone https://github.com/smartgic/shortgic.git
cd shortgic

# Create data directory
mkdir -p data

# Build and start the application
docker-compose up -d
```

The application will be available at `http://localhost:8000`

### 2. Configuration

Copy the example environment file and customize it:

```bash
cp .env.example .env
# Edit .env with your preferred settings
```

### 3. Test the Application

```bash
# Create a short link
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{"target": "https://github.com/smartgic/shortgic"}'

# Response: {"link": "ABC12"}

# Test redirect
curl -L http://localhost:8000/ABC12
```

## Configuration Options

### Environment Variables

| Variable                  | Default             | Description                     |
| ------------------------- | ------------------- | ------------------------------- |
| `SHORTGIC_DATABASE_PATH`  | `/data/shortgic.db` | SQLite database file path       |
| `SHORTGIC_APP_NAME`       | `ShortGic`          | Application name                |
| `SHORTGIC_DEBUG`          | `false`             | Enable debug mode               |
| `SHORTGIC_LINK_LENGTH`    | `5`                 | Length of generated short links |
| `SHORTGIC_MAX_URL_LENGTH` | `2048`              | Maximum URL length allowed      |

### Volume Mounts

- `./data:/data` - Persistent database storage
- `./.env:/app/.env:ro` - Configuration file (optional)

## Production Deployment

### 1. Security Considerations

```bash
# Create secure environment file
cat > .env << EOF
SHORTGIC_DATABASE_PATH=/data/shortgic.db
SHORTGIC_DEBUG=false
SHORTGIC_LINK_LENGTH=6
SHORTGIC_MAX_URL_LENGTH=2048
EOF

# Set proper permissions
chmod 600 .env
```

### 2. Resource Limits

Add resource limits to the shortgic service:

```yaml
shortgic:
  deploy:
    resources:
      limits:
        cpus: "0.5"
        memory: 512M
      reservations:
        cpus: "0.25"
        memory: 256M
```

## Monitoring

### Health Checks

The application includes built-in health checks:

```bash
# Check container health
docker-compose ps

# View health check logs
docker logs shortgic-app
```

## Backup and Recovery

### Database Backup

```bash
# Create backup
docker-compose exec shortgic cp /data/shortgic.db /data/shortgic-backup-$(date +%Y%m%d).db

# Or from host
cp data/shortgic.db data/shortgic-backup-$(date +%Y%m%d).db
```

### Restore Database

```bash
# Stop application
docker-compose stop shortgic

# Restore backup
cp data/shortgic-backup-YYYYMMDD.db data/shortgic.db

# Start application
docker-compose start shortgic
```

## Troubleshooting

### Common Issues

1. **Permission Denied on Database**

   ```bash
   # Fix data directory permissions
   sudo chown -R 1000:1000 data/
   ```

2. **Port Already in Use**

   ```bash
   # Change port in docker-compose.yml
   ports:
     - "8001:8000"  # Use different host port
   ```

3. **Container Won't Start**

   ```bash
   # Check logs
   docker-compose logs shortgic

   # Rebuild image
   docker-compose build --no-cache shortgic
   ```

### Logs

```bash
# View application logs
docker-compose logs -f shortgic

# View all services logs
docker-compose logs -f
```

## Scaling

### Horizontal Scaling

```bash
# Scale to multiple instances
docker-compose up -d --scale shortgic=3
```

Note: When scaling, ensure database consistency and consider using a shared database solution.

## Updates

### Application Updates

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose build shortgic
docker-compose up -d shortgic
```

### System Updates

```bash
# Update all images
docker-compose pull

# Restart with new images
docker-compose up -d
```

## API Documentation

Once running, access the interactive API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Support

For issues and questions:

- GitHub Issues: https://github.com/smartgic/shortgic/issues
- Documentation: https://github.com/smartgic/shortgic
