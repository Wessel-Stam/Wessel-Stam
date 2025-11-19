# Security Documentation

## Overview
This Flask web application implements comprehensive security best practices suitable for a cybersecurity professional's portfolio. The application serves a static portfolio website with enterprise-grade security features.

## Security Features

### 1. HTTPS/TLS Enforcement
- **Flask-Talisman** enforces HTTPS in production
- Self-signed certificates for development (`ssl_context='adhoc'`)
- HSTS (HTTP Strict Transport Security) with 1-year max-age
- Subdomain inclusion for HSTS

### 2. Security Headers
All responses include comprehensive security headers:

- **Content-Security-Policy (CSP)**: Prevents XSS attacks by controlling resource loading
- **X-Content-Type-Options**: Prevents MIME-type sniffing
- **X-Frame-Options**: Prevents clickjacking attacks (set to DENY)
- **X-XSS-Protection**: Browser-level XSS protection for older browsers
- **Strict-Transport-Security (HSTS)**: Enforces HTTPS for 1 year
- **Referrer-Policy**: Controls referrer information leakage
- **Permissions-Policy**: Restricts browser features (geolocation, camera, microphone)

### 3. CSRF Protection
- **Flask-WTF** provides CSRF token validation
- Protects against Cross-Site Request Forgery attacks
- Session-based token management
- Health check endpoint exempted for monitoring

### 4. Rate Limiting
- **Flask-Limiter** prevents abuse and DoS attacks
- Default: 200 requests per day, 50 per hour
- Specific limits per endpoint:
  - Homepage: 30 requests per minute
  - Static files: 100 requests per minute
  - Health check: 10 requests per minute
- IP-based rate limiting

### 5. Session Security
- Secure session cookies (HTTPS only)
- HttpOnly cookies (no JavaScript access)
- SameSite cookie attribute (Lax)
- 24-hour session lifetime
- Cryptographically secure secret key

### 6. Input Validation & Sanitization
- Path traversal prevention
- File extension whitelist for static files
- Maximum request size limit (16MB)
- Request parameter validation

### 7. Error Handling
- Custom error handlers (404, 403, 500)
- No sensitive information in error messages
- Comprehensive logging for security monitoring
- Server header removal

### 8. Logging & Monitoring
- Structured logging with timestamps
- Security event logging (unauthorized access attempts)
- Error tracking
- Health check endpoint for monitoring

### 9. Dependency Security
All dependencies are pinned to specific versions:
- Flask 3.0.0
- Flask-Talisman 1.1.0
- Flask-Limiter 3.5.0
- Flask-WTF 1.2.1
- Gunicorn 21.2.0 (production server)

### 10. Container Security (Docker)
- Multi-stage build (smaller attack surface)
- Non-root user execution
- Read-only filesystem
- Dropped capabilities (principle of least privilege)
- Health checks
- No new privileges
- Minimal base image (python:3.11-slim)

## Configuration

### Environment Variables
Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

**Critical**: Generate a secure SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Production Deployment Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Generate and set a secure `SECRET_KEY`
- [ ] Configure SSL/TLS certificates
- [ ] Enable HTTPS enforcement
- [ ] Set up reverse proxy (nginx/Apache)
- [ ] Configure firewall rules
- [ ] Enable security monitoring
- [ ] Set up automated backups
- [ ] Configure log aggregation
- [ ] Enable intrusion detection
- [ ] Implement DDoS protection
- [ ] Regular dependency updates
- [ ] Security audit and penetration testing

## Running the Application

### Development Mode
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python run.py
```

Development server includes:
- Self-signed SSL certificate
- Debug mode enabled
- Relaxed security settings
- Not suitable for production

### Production Mode
```bash
# Using Gunicorn (recommended)
gunicorn -c gunicorn.conf.py app:app

# Using Docker
docker-compose up -d

# Using Docker build
docker build -t portfolio-webapp .
docker run -p 5000:5000 -e SECRET_KEY=your-secret-key portfolio-webapp
```

## Security Best Practices

### 1. Secret Management
- Never commit secrets to version control
- Use environment variables or secret management services
- Rotate secrets regularly
- Use different secrets for different environments

### 2. HTTPS Configuration
- Use valid SSL/TLS certificates in production
- Use Let's Encrypt for free certificates
- Configure strong cipher suites
- Disable outdated protocols (SSL, TLS 1.0, TLS 1.1)

### 3. Reverse Proxy Setup
Recommended nginx configuration:
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4. Regular Updates
```bash
# Check for security vulnerabilities
pip install safety
safety check

# Update dependencies
pip install -U -r requirements.txt
```

### 5. Monitoring
- Monitor application logs
- Set up alerts for suspicious activity
- Track rate limit violations
- Monitor system resources

## Security Testing

### Manual Testing
1. Test HTTPS enforcement
2. Verify security headers
3. Test rate limiting
4. Attempt path traversal
5. Test CSRF protection
6. Verify error handling

### Automated Testing
```bash
# Run security scanner
pip install bandit
bandit -r app.py

# Check dependencies
pip install safety
safety check
```

## Incident Response

If you suspect a security incident:
1. Isolate affected systems
2. Review logs for indicators of compromise
3. Rotate all secrets and credentials
4. Investigate root cause
5. Patch vulnerabilities
6. Document findings
7. Update security measures

## Compliance

This application implements security controls aligned with:
- OWASP Top 10
- CIS Security Benchmarks
- NIST Cybersecurity Framework

## Contact

For security concerns or vulnerability reports:
- Review logs in application output
- Check health endpoint: `/health`
- Monitor rate limiting events

## References

- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/latest/security/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)
