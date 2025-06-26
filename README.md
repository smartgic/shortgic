# 🚀 ShortGic - Lightning Fast URL Shortener

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-pink.svg?style=flat)](https://github.com/smartgic/shortgic/pulls) [![Discord](https://img.shields.io/discord/809074036733902888)](https://discord.gg/Vu7Wmd9j)

> **Transform long URLs into short, shareable links in milliseconds** ⚡

ShortGic is a **blazingly fast**, **enterprise-ready** URL shortener built with modern Python. Perfect for developers, businesses, and anyone who needs reliable link management.

## ✨ Why Choose ShortGic?

- 🔥 **Ultra Fast** - Built with FastAPI for maximum performance
- 🛡️ **Enterprise Security** - Cryptographically secure link generation
- 🎯 **Zero Dependencies** - SQLite database, no external services needed
- 🔧 **Developer Friendly** - RESTful API with automatic documentation
- 📦 **Docker Ready** - Deploy anywhere in seconds
- 🎨 **Customizable** - Environment-based configuration
- 📊 **Production Ready** - Comprehensive error handling and validation

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Run instantly with Docker
docker run -d --name shortgic -p 8000:8000 smartgic/shortgic:latest

# Your URL shortener is now live at http://localhost:8000
```

### Option 2: Local Installation

```bash
# Clone and setup
git clone https://github.com/smartgic/shortgic.git
cd shortgic
pip install -r requirements.txt

# Launch in seconds
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**That's it!** 🎉 Your URL shortener is running at `http://localhost:8000`

## 💡 Usage Examples

### Create Short Links

```bash
# Basic URL shortening
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{"target": "https://your-very-long-url.com/with/many/parameters"}'

# Response: {"link": "ABC12"}
```

### Add Metadata (Perfect for Analytics)

```bash
# Track campaigns, versions, or any custom data
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{
    "target": "https://smartgic.io",
    "extras": {
      "campaign": "summer-2024",
      "source": "email",
      "validated": true
    }
  }'
```

### Access Your Links

```bash
# Redirect to original URL
curl -L http://localhost:8000/ABC12

# Get link information and metadata
curl http://localhost:8000/ABC12/info
```

### Manage Links

```bash
# Delete a link permanently
curl -X DELETE http://localhost:8000/ABC12
```

## 🎯 Perfect For

- **Developers** - Clean API for integration into any application
- **Marketers** - Track campaigns with custom metadata
- **Businesses** - Self-hosted solution with full control
- **Content Creators** - Shorten links for social media
- **Teams** - Internal link management and sharing

## 🔧 Advanced Configuration

Customize ShortGic with environment variables:

```bash
# Database location
export SHORTGIC_DATABASE_PATH="./my-links.db"

# Link length (default: 5 characters)
export SHORTGIC_LINK_LENGTH=8

# Maximum URL length (default: 2048)
export SHORTGIC_MAX_URL_LENGTH=4096

# Debug mode
export SHORTGIC_DEBUG=true
```

## 📚 API Documentation

ShortGic automatically generates beautiful, interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🏗️ Production Deployment

### Docker Compose

```yaml
version: "3.8"
services:
  shortgic:
    image: smartgic/shortgic:latest
    ports:
      - "8000:8000"
    environment:
      - SHORTGIC_DATABASE_PATH=/data/shortgic.db
    volumes:
      - ./data:/data
    restart: unless-stopped
```

### Environment Variables

```bash
# Production settings
SHORTGIC_DATABASE_PATH=/var/lib/shortgic/shortgic.db
SHORTGIC_DEBUG=false
SHORTGIC_LINK_LENGTH=6
```

## 🛡️ Security Features

- **Cryptographically Secure** - Uses Python's `secrets` module for link generation
- **Input Validation** - Comprehensive URL and format validation
- **Error Handling** - Detailed error responses without information leakage
- **No External Dependencies** - Reduces attack surface

## 🚀 Performance

- **Sub-millisecond** response times
- **Optimized database** queries with proper indexing
- **Efficient collision** handling for unique link generation
- **Memory efficient** with minimal resource usage

## 🤝 Contributing

We love contributions! Whether it's:

- 🐛 Bug reports
- 💡 Feature requests
- 📖 Documentation improvements
- 🔧 Code contributions

Check out our [contribution guidelines](https://github.com/smartgic/shortgic/pulls) and join our [Discord community](https://discord.gg/Vu7Wmd9j)!

## 📄 License

Apache License 2.0 - feel free to use ShortGic in your projects, commercial or otherwise.

---

**Ready to shorten your first URL?** 🎯

```bash
docker run -d -p 8000:8000 smartgic/shortgic:latest
```

_Made with ❤️ by the Smart'Gic team_
