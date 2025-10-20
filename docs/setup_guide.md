# Setup Guide

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Git for version control
- Command line access (Command Prompt, PowerShell, or Terminal)
- Text editor or IDE (VS Code recommended)

### Account Requirements
- OneLogin developer account (for production use)
- GitHub account (for repository access)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Noble-Antwi/onelogin-sso-integration.git
cd onelogin-sso-integration
```

### 2. Create Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Verify Installation

Run the configuration test to ensure everything is set up correctly:

```bash
python test_config.py
```

Expected output should show directories exist and basic configuration is loaded.

## Configuration

### Development Configuration

The system runs in demo mode by default, which allows testing without real OneLogin credentials.

To verify demo mode is working:
```bash
python test_saml_basic.py
```

### Production Configuration

For production deployment with real OneLogin integration:

1. **Copy the configuration template:**
   ```bash
   cp config/saml_settings.json.template config/saml_settings.json
   ```

2. **Edit the configuration file** with your OneLogin credentials:
   ```json
   {
     "onelogin": {
       "client_id": "YOUR_ACTUAL_CLIENT_ID",
       "client_secret": "YOUR_ACTUAL_CLIENT_SECRET",
       "region": "us",
       "subdomain": "your-company-subdomain"
     }
   }
   ```

3. **Set environment variables** (recommended for security):
   ```bash
   set ONELOGIN_CLIENT_ID=your_client_id
   set ONELOGIN_CLIENT_SECRET=your_client_secret
   set ONELOGIN_SUBDOMAIN=your_subdomain
   ```

### Application Configuration

The system includes three pre-configured applications:
- HR Management System
- Payroll System  
- Employee Portal

To modify applications, edit the `applications` section in `config/settings.py`.

## Testing

### Component Testing

Test individual components:

```bash
# Test configuration system
python test_config.py

# Test SAML handler
python test_saml_basic.py

# Test OneLogin connector
python test_onelogin.py

# Test complete provisioning system
python test_provisioning.py
```

### Running All Tests

```bash
pytest tests/ -v
```

### Generating Test Reports

The provisioning test automatically generates detailed reports in the `logs/` directory.

## Troubleshooting

### Common Issues

**ModuleNotFoundError: No module named 'requests'**
- Solution: Ensure virtual environment is activated and dependencies are installed
- Run: `python -m pip install -r requirements.txt`

**Configuration not found warnings**
- Expected in demo mode
- For production, ensure `config/saml_settings.json` exists with valid credentials

**Permission errors on Windows**
- Run command prompt as Administrator
- Ensure Python has write permissions to the project directory

### Log Files

Application logs are written to `logs/sso_integration.log`. Check this file for detailed error information.

### Debug Mode

Enable debug logging by setting the environment variable:
```bash
set LOG_LEVEL=DEBUG
```

## Development Workflow

### Adding New Features

1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement changes
3. Add tests for new functionality
4. Update documentation
5. Submit pull request

### Code Style

- Follow PEP 8 Python style guidelines
- Use type hints for function parameters and returns
- Include docstrings for all classes and methods
- Maintain consistent logging format

## Security Considerations

### Credential Management

- Never commit actual OneLogin credentials to version control
- Use environment variables for sensitive configuration
- The `.gitignore` file excludes `config/saml_settings.json` from commits

### Token Security

- Access tokens are stored in memory only
- Tokens expire automatically after 1 hour
- Session data is not persisted to disk in demo mode

## Performance Optimization

### Bulk Operations

- Use `provision_users_bulk()` for processing multiple users
- Monitor performance metrics in generated reports
- Consider implementing batch size limits for very large user sets

### Caching

- OneLogin tokens are cached until expiration
- SAML sessions are maintained in memory
- Clear caches during development: restart the application

## Production Deployment

### Environment Setup

1. Configure production OneLogin application
2. Set up secure credential storage
3. Configure logging to production log management system
4. Implement monitoring and alerting

### Database Configuration

For production use, replace in-memory storage with persistent database:
- Update `config/settings.py` database configuration
- Implement database migration scripts
- Configure backup and recovery procedures

### Scaling Considerations

- Implement connection pooling for high-volume operations
- Consider load balancing for multiple application instances
- Monitor API rate limits and implement backoff strategies

## Support

### Documentation

- [Architecture Overview](architecture.md)
- [Troubleshooting Guide](troubleshooting.md)
- [API Reference](../src/)

### Resources

- OneLogin Developer Documentation: https://developers.onelogin.com/
- SAML 2.0 Specification: https://docs.oasis-open.org/security/saml/
- Python SAML Library: https://github.com/onelogin/python3-saml