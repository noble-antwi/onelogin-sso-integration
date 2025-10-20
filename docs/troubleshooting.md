# Troubleshooting Guide

## Common Issues and Solutions

### Installation and Setup Issues

#### Python Version Compatibility

**Issue:** `SyntaxError` or compatibility warnings during installation

**Symptoms:**
- Import errors with type hints
- Module not found errors for standard libraries
- Syntax errors in f-strings

**Solution:**
1. Verify Python version: `python --version`
2. Ensure Python 3.8 or higher is installed
3. Update Python if necessary
4. Recreate virtual environment with correct Python version

#### Virtual Environment Issues

**Issue:** Package installation failures or module import errors

**Symptoms:**
- `ModuleNotFoundError` for installed packages
- Permission denied errors
- Packages installing globally instead of in virtual environment

**Solution:**
1. Verify virtual environment is activated
2. Check for virtual environment indicator in command prompt
3. Recreate virtual environment if corrupted:
   ```bash
   deactivate
   rmdir /s venv
   python -m venv venv
   venv\Scripts\activate
   python -m pip install -r requirements.txt
   ```

#### Dependency Installation Failures

**Issue:** `pip install` commands fail or timeout

**Symptoms:**
- Network timeout errors
- SSL certificate errors
- Package version conflicts

**Solutions:**
1. **Network Issues:**
   ```bash
   python -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
   ```

2. **Version Conflicts:**
   ```bash
   python -m pip install --upgrade pip
   python -m pip install --force-reinstall -r requirements.txt
   ```

3. **Corporate Firewall:**
   Configure pip to use corporate proxy settings

### Configuration Issues

#### Missing Configuration Files

**Issue:** `No config file found, using defaults` warning

**Symptoms:**
- System runs in demo mode only
- OneLogin integration not working
- Default configuration values used

**Solution:**
1. **For Demo Mode:** This is expected behavior, no action needed
2. **For Production:** Create configuration file:
   ```bash
   cp config/saml_settings.json.template config/saml_settings.json
   ```
3. Edit the file with actual OneLogin credentials

#### Invalid OneLogin Credentials

**Issue:** Authentication failures with OneLogin API

**Symptoms:**
- `Authentication failed` errors
- HTTP 401 responses from OneLogin
- Empty or invalid tokens

**Troubleshooting Steps:**
1. **Verify Credentials:**
   - Check client ID format (should be alphanumeric)
   - Verify client secret is complete
   - Confirm subdomain matches OneLogin account

2. **Check Environment Variables:**
   ```bash
   echo %ONELOGIN_CLIENT_ID%
   echo %ONELOGIN_CLIENT_SECRET%
   echo %ONELOGIN_SUBDOMAIN%
   ```

3. **Test API Connectivity:**
   ```bash
   python test_onelogin.py
   ```

#### File Permission Errors

**Issue:** Cannot write to logs directory or configuration files

**Symptoms:**
- `PermissionError` when writing logs
- Configuration file creation failures
- Report generation errors

**Solutions:**
1. **Windows:**
   - Run command prompt as Administrator
   - Check folder permissions
   - Ensure antivirus is not blocking file creation

2. **Linux/macOS:**
   ```bash
   chmod 755 logs/
   chmod 644 config/
   ```

### Runtime Issues

#### SAML Handler Errors

**Issue:** SAML request generation or validation failures

**Symptoms:**
- Invalid XML errors
- Base64 encoding/decoding errors
- Session creation failures

**Diagnostic Steps:**
1. **Test SAML Handler:**
   ```bash
   python test_saml_basic.py
   ```

2. **Check XML Format:**
   - Verify entity ID format
   - Confirm URL endpoints are accessible
   - Validate timestamp formats

3. **Session Issues:**
   - Clear session storage: restart application
   - Check session timeout settings
   - Verify session ID generation

#### OneLogin API Errors

**Issue:** API calls failing or returning unexpected responses

**Common Error Codes:**
- **401 Unauthorized:** Invalid credentials or expired token
- **403 Forbidden:** Insufficient permissions
- **429 Too Many Requests:** Rate limit exceeded
- **500 Internal Server Error:** OneLogin service issues

**Solutions by Error Code:**

**401 Unauthorized:**
1. Verify API credentials
2. Check token expiration
3. Re-authenticate: restart application

**403 Forbidden:**
1. Verify OneLogin app permissions
2. Check API scope settings
3. Contact OneLogin administrator

**429 Rate Limit:**
1. Implement request delays
2. Reduce batch sizes
3. Monitor API usage patterns

**500 Server Error:**
1. Check OneLogin status page
2. Retry with exponential backoff
3. Contact OneLogin support if persistent

#### User Provisioning Failures

**Issue:** Bulk provisioning operations failing partially or completely

**Symptoms:**
- Some users created, others failed
- Timeout errors during bulk operations
- Inconsistent user data

**Troubleshooting:**
1. **Check Individual User Data:**
   ```python
   # Test single user provisioning
   single_result = engine.provision_single_user(problem_user)
   print(single_result)
   ```

2. **Validate User Data Format:**
   - Ensure required fields are present
   - Check email format validity
   - Verify character encoding

3. **Reduce Batch Size:**
   - Process smaller batches
   - Monitor memory usage
   - Check for rate limiting

### Performance Issues

#### Slow Bulk Operations

**Issue:** User provisioning taking longer than expected

**Symptoms:**
- Operations timing out
- High memory usage
- Slow API response times

**Optimization Steps:**
1. **Monitor Performance:**
   ```bash
   python test_provisioning.py
   ```
   Check performance metrics in output

2. **Reduce Batch Size:**
   - Process 50-100 users per batch instead of larger amounts
   - Implement progress tracking
   - Add delays between batches

3. **Optimize Network:**
   - Check internet connection speed
   - Monitor OneLogin API response times
   - Consider geographic proximity to OneLogin servers

#### Memory Usage Issues

**Issue:** High memory consumption during operations

**Symptoms:**
- Application becoming unresponsive
- System running out of memory
- Slow performance

**Solutions:**
1. **Monitor Memory Usage:**
   - Use Task Manager (Windows) or Activity Monitor (macOS)
   - Check for memory leaks
   - Monitor garbage collection

2. **Optimize Code:**
   - Process users in smaller batches
   - Clear session storage periodically
   - Implement memory-efficient data structures

### Debugging Techniques

#### Enable Debug Logging

1. **Set Environment Variable:**
   ```bash
   set LOG_LEVEL=DEBUG
   ```

2. **Check Log Files:**
   ```bash
   type logs\sso_integration.log
   ```

3. **Monitor Real-time Logs:**
   ```bash
   tail -f logs/sso_integration.log
   ```

#### API Request Debugging

1. **Add Request Logging:**
   ```python
   import logging
   logging.getLogger("requests").setLevel(logging.DEBUG)
   ```

2. **Capture HTTP Traffic:**
   - Use network monitoring tools
   - Check request/response headers
   - Verify payload format

#### Configuration Debugging

1. **Validate Configuration:**
   ```bash
   python test_config.py
   ```

2. **Check Environment Variables:**
   ```bash
   set | findstr ONELOGIN
   ```

3. **Test Configuration Loading:**
   ```python
   from config.settings import config
   print(config.validate_config())
   ```

### Error Message Reference

#### Common Error Messages and Solutions

**"No module named 'requests'"**
- **Cause:** Missing dependency
- **Solution:** `python -m pip install requests`

**"Config file not found, using defaults"**
- **Cause:** Missing configuration file
- **Solution:** Normal in demo mode, create config file for production

**"Authentication failed"**
- **Cause:** Invalid OneLogin credentials
- **Solution:** Verify credentials and network connectivity

**"Session not found"**
- **Cause:** Session expired or invalid
- **Solution:** Re-authenticate user

**"Permission denied"**
- **Cause:** File system permissions
- **Solution:** Run with administrator privileges or fix file permissions

**"Connection timeout"**
- **Cause:** Network connectivity issues
- **Solution:** Check internet connection and firewall settings

### Advanced Troubleshooting

#### Network Connectivity Issues

1. **Test OneLogin Connectivity:**
   ```bash
   ping api.us.onelogin.com
   nslookup api.us.onelogin.com
   ```

2. **Check Firewall Settings:**
   - Ensure ports 80 and 443 are open
   - Verify HTTPS traffic is allowed
   - Check corporate proxy settings

3. **SSL Certificate Issues:**
   ```bash
   python -c "import ssl; import urllib.request; urllib.request.urlopen('https://api.us.onelogin.com')"
   ```

#### Database and Storage Issues

1. **Check Disk Space:**
   ```bash
   dir logs\
   ```

2. **Verify File Permissions:**
   ```bash
   icacls logs\
   ```

3. **Clear Temporary Files:**
   ```bash
   del logs\*.tmp
   ```

### Getting Additional Help

#### Log Collection for Support

When reporting issues, collect the following information:

1. **System Information:**
   ```bash
   python --version
   python -m pip list
   ```

2. **Configuration Status:**
   ```bash
   python test_config.py > system_status.txt
   ```

3. **Error Logs:**
   ```bash
   copy logs\sso_integration.log error_logs.txt
   ```

4. **Test Results:**
   ```bash
   python test_saml_basic.py > test_results.txt
   ```

#### Support Resources

- **OneLogin Developer Documentation:** https://developers.onelogin.com/
- **Python SAML Library Issues:** https://github.com/onelogin/python3-saml/issues
- **Project Repository Issues:** GitHub Issues section

#### Creating Support Tickets

Include the following information when creating support tickets:

1. **Environment Details:**
   - Operating system and version
   - Python version
   - Dependency versions

2. **Error Description:**
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages and stack traces

3. **Configuration:**
   - Anonymized configuration files
   - Environment variable settings (without sensitive values)
   - Test results and logs