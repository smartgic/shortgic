# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive GitHub Actions workflows for CI/CD
- Security scanning with CodeQL, Trivy, and dependency checks
- Performance testing with Locust and pytest-benchmark
- Automated dependency updates with Renovate
- Docker Compose deployment configuration
- Environment-based configuration system

### Changed
- Improved database initialization and error handling
- Enhanced security with cryptographically secure random generation
- Optimized database queries with proper indexing

### Fixed
- Database creation issues when file doesn't exist
- Proper error handling for invalid URLs
- Memory leaks in database connections

### Security
- Added comprehensive security scanning
- Implemented secure random link generation
- Added vulnerability monitoring

## [v1.0.0] - 2024-01-01

### Added
- Initial release of ShortGic URL shortener
- FastAPI-based REST API
- SQLite database backend
- Docker containerization
- Basic URL shortening and redirection functionality
- Health check endpoints
- API documentation with Swagger UI

### Features
- Create short links from long URLs
- Redirect short links to original URLs
- Configurable link length
- URL validation
- Database persistence
- RESTful API design

### Technical
- Python 3.11+ support
- FastAPI framework
- SQLAlchemy ORM
- Pydantic data validation
- Docker multi-stage builds
- Non-root container execution

[Unreleased]: https://github.com/smartgic/shortgic/compare/v1.0.0...HEAD
[v1.0.0]: https://github.com/smartgic/shortgic/releases/tag/v1.0.0
