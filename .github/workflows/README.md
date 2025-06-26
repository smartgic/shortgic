# GitHub Actions Workflows

This directory contains comprehensive GitHub Actions workflows for the ShortGic URL shortener application. These workflows provide automated CI/CD, security scanning, performance testing, and dependency management.

## 📋 Workflow Overview

| Workflow | Purpose | Triggers | Status |
|----------|---------|----------|--------|
| [CI/CD Pipeline](#cicd-pipeline) | Main build, test, and deployment | Push, PR, Release | Core |
| [Security Scan](#security-scan) | Security vulnerability scanning | Daily, Push, PR | Security |
| [Dependency Updates](#dependency-updates) | Automated dependency management | Weekly, Manual | Maintenance |
| [Performance Testing](#performance-testing) | Load testing and benchmarks | Weekly, Push to main | Performance |
| [Release](#release) | Automated release management | Tags, Manual | Release |

## 🚀 CI/CD Pipeline

**File:** `ci.yml`

### Features
- **Multi-Python Testing**: Tests across Python 3.11, 3.12, and 3.13
- **Code Quality**: Black, isort, flake8, mypy, bandit, safety
- **Docker Testing**: Build and functional testing
- **Security Scanning**: Trivy container scanning
- **Automated Publishing**: GitHub Container Registry
- **Deployment**: Staging and production environments

### Triggers
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Release events

### Jobs
1. **Test Suite**: Unit tests with coverage across Python versions
2. **Code Quality**: Linting, formatting, type checking, security analysis
3. **Docker Build & Test**: Container build and functional testing
4. **Publish**: Docker image publishing to GHCR
5. **Deploy**: Staging and production deployment

### Environment Variables
```yaml
PYTHON_VERSION: '3.13'
DOCKER_IMAGE: shortgic
REGISTRY: ghcr.io
```

## 🔒 Security Scan

**File:** `security.yml`

### Features
- **CodeQL Analysis**: GitHub's semantic code analysis
- **Dependency Scanning**: Safety and pip-audit checks
- **Container Security**: Trivy vulnerability scanning
- **Secrets Detection**: TruffleHog secret scanning
- **License Compliance**: License compatibility checking

### Triggers
- Daily at 2 AM UTC
- Push to `main` or `develop` branches
- Pull requests
- Manual dispatch

### Jobs
1. **CodeQL**: Static analysis for security vulnerabilities
2. **Dependency Check**: Python package vulnerability scanning
3. **Docker Security**: Container image vulnerability assessment
4. **Secrets Scan**: Repository secret detection
5. **License Check**: License compliance verification
6. **Security Summary**: Consolidated security report

### Security Reports
- SARIF files uploaded to GitHub Security tab
- Artifact reports for detailed analysis
- Step summaries with key findings

## 🔄 Dependency Updates

**File:** `dependency-update.yml`

### Features
- **Python Dependencies**: pip-tools for requirement updates
- **GitHub Actions**: Renovate for action updates
- **Security Auditing**: Post-update vulnerability checks
- **Automated PRs**: Pull requests for approved updates
- **Test Validation**: Ensures updates don't break functionality

### Triggers
- Weekly on Mondays at 9 AM UTC
- Manual dispatch

### Jobs
1. **Update Dependencies**: Python package updates with pip-compile
2. **Update GitHub Actions**: Renovate-based action updates
3. **Security Audit**: Post-update security validation

### Automation
- Creates PRs for dependency updates
- Runs tests before creating PRs
- Creates security issues for vulnerabilities

## ⚡ Performance Testing

**File:** `performance.yml`

### Features
- **Load Testing**: Locust-based load testing
- **Benchmark Testing**: pytest-benchmark performance tests
- **Memory Profiling**: Memory usage analysis
- **Performance Comparison**: PR performance comparison

### Triggers
- Push to `main` branch
- Pull requests to `main`
- Weekly on Sundays at 3 AM UTC
- Manual dispatch

### Jobs
1. **Load Test**: Simulated user load testing
2. **Benchmark Test**: Micro-benchmark performance testing
3. **Memory Profiling**: Memory usage analysis
4. **Performance Comparison**: PR vs main comparison

### Test Scenarios
- **Load Test**: 50 concurrent users, 2-minute duration
- **Benchmark**: Link creation, access, health check timing
- **Memory**: 100 link creation and access cycles

## 🎯 Release

**File:** `release.yml`

### Features
- **Release Validation**: Tag format and changelog validation
- **Comprehensive Testing**: Full test suite before release
- **GitHub Releases**: Automated release creation
- **Docker Publishing**: Multi-tag container publishing
- **Security Scanning**: Release-specific security validation

### Triggers
- Git tags matching `v*` pattern
- Manual dispatch with version input

### Jobs
1. **Validate Release**: Tag format and changelog validation
2. **Build and Test**: Comprehensive testing
3. **Create Release**: GitHub release with notes
4. **Publish Docker**: Multi-tag container publishing
5. **Security Scan**: Release security validation
6. **Notify**: Release summary and notifications

### Release Process
1. Tag validation (semantic versioning)
2. Changelog verification
3. Full test suite execution
4. Docker image building and testing
5. GitHub release creation
6. Container registry publishing
7. Security scanning
8. Notification and summary

## 🛠️ Configuration Files

### Renovate Configuration
**File:** `renovate.json`

```json
{
  "schedule": ["before 6am on monday"],
  "packageRules": [
    {
      "matchManagers": ["pip_requirements"],
      "groupName": "Python dependencies"
    },
    {
      "matchManagers": ["github-actions"],
      "groupName": "GitHub Actions",
      "automerge": true
    }
  ]
}
```

### Workflow Secrets
Required repository secrets:
- `GITHUB_TOKEN`: Automatically provided
- Additional secrets for deployment environments

## 📊 Monitoring and Reporting

### Artifacts Generated
- **Test Coverage**: XML and HTML coverage reports
- **Security Reports**: SARIF files, JSON reports
- **Performance Results**: HTML reports, CSV data
- **Benchmark Data**: JSON results, histograms
- **Memory Profiles**: Detailed memory usage reports

### GitHub Integration
- **Security Tab**: SARIF uploads for vulnerability tracking
- **Releases**: Automated release notes and assets
- **Packages**: Container registry integration
- **Actions**: Workflow status and summaries

## 🔧 Customization

### Environment-Specific Configuration
Modify environment variables in workflow files:

```yaml
env:
  PYTHON_VERSION: '3.13'
  DOCKER_IMAGE: shortgic
  REGISTRY: ghcr.io
```

### Adding New Tests
1. Add test files to appropriate directories
2. Update workflow test commands
3. Configure artifact collection

### Deployment Customization
Update deployment jobs with your infrastructure:

```yaml
deploy-production:
  steps:
    - name: Deploy to production
      run: |
        # Add your deployment commands
        kubectl apply -f k8s/
```

## 🚨 Troubleshooting

### Common Issues

1. **Test Failures**
   - Check test logs in workflow runs
   - Verify database permissions
   - Ensure environment variables are set

2. **Docker Build Issues**
   - Check Dockerfile syntax
   - Verify base image availability
   - Review build context

3. **Security Scan Failures**
   - Review vulnerability reports
   - Update dependencies
   - Check for false positives

4. **Performance Degradation**
   - Compare benchmark results
   - Review memory profiles
   - Check for resource constraints

### Debug Mode
Enable debug logging by setting:
```yaml
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

## 📈 Best Practices

### Workflow Optimization
- Use caching for dependencies
- Parallel job execution
- Conditional job execution
- Resource-appropriate runners

### Security
- Minimal required permissions
- Secret management
- Vulnerability monitoring
- Regular security updates

### Performance
- Efficient test execution
- Parallel testing strategies
- Resource monitoring
- Performance regression detection

## 🔗 Related Documentation

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Best Practices](../README-Docker.md)
- [Security Guidelines](../SECURITY.md)
- [Contributing Guidelines](../CONTRIBUTING.md)

---

For questions or issues with the workflows, please create an issue in the repository or refer to the GitHub Actions documentation.
