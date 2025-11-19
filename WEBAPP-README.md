# Secure Portfolio Web Application 🔒

A production-ready, security-hardened Flask web application serving a professional portfolio website. Built with cybersecurity best practices by an Information Security Officer.

## 🛡️ Security Features

This application implements enterprise-grade security features:

### Core Security
- ✅ **HTTPS/TLS Enforcement** - Automatic HTTPS redirection with HSTS
- ✅ **Security Headers** - Comprehensive HTTP security headers (CSP, X-Frame-Options, etc.)
- ✅ **CSRF Protection** - Token-based protection against cross-site request forgery
- ✅ **Rate Limiting** - IP-based rate limiting to prevent abuse and DoS attacks
- ✅ **Session Security** - Secure, HttpOnly, SameSite cookies with expiration
- ✅ **Input Validation** - Path traversal prevention and file type whitelisting
- ✅ **XSS Protection** - Content Security Policy and output sanitization
- ✅ **Clickjacking Protection** - X-Frame-Options header
- ✅ **MIME Sniffing Prevention** - X-Content-Type-Options header

### Infrastructure Security
- ✅ **Non-root User** - Container runs as unprivileged user
- ✅ **Read-only Filesystem** - Minimal write permissions
- ✅ **Capability Dropping** - Minimal Linux capabilities
- ✅ **Health Checks** - Automated health monitoring
- ✅ **Secure Logging** - Comprehensive security event logging

### Dependencies
- ✅ **Pinned Versions** - All dependencies locked to specific versions
- ✅ **Minimal Attack Surface** - Only essential packages included
- ✅ **Regular Updates** - Easy update path with requirements.txt

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip
- Docker (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/Wessel-Stam/Wessel-Stam.git
cd Wessel-Stam

# Run automated setup
chmod +x setup.sh
./setup.sh

# Or manual setup
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set SECRET_KEY

# Generate secure secret key
python -c "import secrets; print(secrets.token_hex(32))"
```

### Running the Application

#### Development Mode
```bash
python run.py
```
Access at: `https://localhost:5000` (accepts self-signed certificate)

#### Production Mode
```bash
# Using Gunicorn (recommended)
gunicorn -c gunicorn.conf.py app:app

# Using Docker
docker-compose up -d

# Check status
curl http://localhost:5000/health
```

## 📋 Project Structure

```
.
├── app.py                  # Main Flask application with security features
├── config.py               # Security configuration
├── run.py                  # Development server runner
├── gunicorn.conf.py        # Production server configuration
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container image definition
├── docker-compose.yml      # Container orchestration
├── setup.sh                # Automated setup script
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── SECURITY.md             # Security documentation
├── DEPLOYMENT.md           # Deployment guide
├── WEBAPP-README.md        # This file
├── index.html              # Portfolio website
├── styles.css              # Styling
├── script.js               # Interactive features
├── README.md               # GitHub profile README
└── PORTFOLIO-README.md     # Portfolio documentation
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file from `.env.example`:

```bash
# Flask Configuration
FLASK_ENV=development      # Set to 'production' in production
SECRET_KEY=your-secret-key # Generate with: python -c "import secrets; print(secrets.token_hex(32))"

# Server Configuration
PORT=5000
HOST=0.0.0.0

# Security Settings
FORCE_HTTPS=false          # Set to 'true' in production

# Rate Limiting
RATELIMIT_STORAGE_URL=memory://

# Logging
LOG_LEVEL=INFO
```

### Security Configuration

Edit `config.py` to customize:
- Content Security Policy
- Rate limiting thresholds
- Session timeout
- CORS settings
- Security headers

## 🐳 Docker Deployment

### Build and Run
```bash
# Build image
docker build -t portfolio-webapp .

# Run container
docker run -d \
  -p 5000:5000 \
  -e SECRET_KEY=your-secret-key \
  -e FLASK_ENV=production \
  --name portfolio \
  portfolio-webapp

# Or use docker-compose
docker-compose up -d
```

### Security Features in Docker
- Multi-stage build (smaller image)
- Non-root user execution
- Read-only filesystem
- Dropped capabilities
- Health checks
- No new privileges
- Minimal base image

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{"status": "healthy", "service": "portfolio-webapp"}
```

### Logs
```bash
# Docker
docker-compose logs -f webapp

# Direct
tail -f app.log
```

### Metrics
- Request count and rate limits
- Error rates
- Response times
- Security events

## 🔐 Security Best Practices

### Development
- Use self-signed certificates (automatic)
- Debug mode enabled
- Relaxed HTTPS enforcement
- Detailed error messages

### Production
- Valid SSL/TLS certificates (Let's Encrypt)
- Debug mode disabled
- Strict HTTPS enforcement
- Generic error messages
- Use Gunicorn with multiple workers
- Deploy behind reverse proxy (nginx)
- Configure firewall rules
- Enable monitoring and alerts
- Regular security updates

### Secret Management
```bash
# Generate secure secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Never commit secrets to git
# Use environment variables or secret management service
# Rotate secrets regularly
```

## 🧪 Testing

### Security Testing
```bash
# Check for vulnerabilities
pip install safety
safety check

# Static analysis
pip install bandit
bandit -r app.py

# Test security headers
curl -I https://localhost:5000
```

### Manual Testing
- [ ] HTTPS enforcement
- [ ] Security headers present
- [ ] Rate limiting works
- [ ] Path traversal blocked
- [ ] Invalid file types rejected
- [ ] CSRF protection active
- [ ] Error handling correct

## 📚 Documentation

- **[SECURITY.md](SECURITY.md)** - Comprehensive security documentation
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Detailed deployment guide
- **[PORTFOLIO-README.md](PORTFOLIO-README.md)** - Portfolio website documentation

## 🛠️ Technology Stack

### Backend
- **Flask 3.0** - Web framework
- **Gunicorn 21.2** - WSGI HTTP server
- **Python 3.11** - Programming language

### Security Libraries
- **Flask-Talisman** - HTTPS and security headers
- **Flask-Limiter** - Rate limiting
- **Flask-WTF** - CSRF protection
- **pyOpenSSL** - SSL/TLS support

### Infrastructure
- **Docker** - Containerization
- **Nginx** - Reverse proxy (recommended)
- **Systemd** - Service management

## 🚦 Rate Limits

Default limits per endpoint:

| Endpoint | Limit |
|----------|-------|
| Homepage (/) | 30 per minute |
| Static files | 100 per minute |
| Health check | 10 per minute |
| Global | 200 per day, 50 per hour |

Limits are IP-based and configurable in `app.py`.

## 🔄 Maintenance

### Update Dependencies
```bash
# Check for updates
pip list --outdated

# Update all
pip install -U -r requirements.txt

# Test after updating
python -m pytest
```

### Security Updates
```bash
# Check for vulnerabilities
safety check

# Update vulnerable packages
pip install --upgrade package-name
```

### Backup
```bash
# Backup configuration
tar -czf backup-$(date +%Y%m%d).tar.gz .env *.py *.html *.css *.js

# Restore
tar -xzf backup-YYYYMMDD.tar.gz
```

## 🐛 Troubleshooting

### Common Issues

**Port already in use**
```bash
lsof -i :5000
kill -9 <PID>
```

**SSL certificate errors (development)**
```bash
pip install pyopenssl --upgrade
```

**Module not found**
```bash
pip install -r requirements.txt --upgrade
```

**Permission denied**
```bash
chmod +x run.py setup.sh
```

### Debug Mode
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python run.py
```

## 📈 Performance

### Optimization Tips
- Use Gunicorn with multiple workers
- Enable caching headers
- Use CDN for static assets
- Implement Redis for rate limiting
- Use connection pooling
- Enable gzip compression in nginx

### Scaling
- Horizontal: Multiple instances + load balancer
- Vertical: Increase instance resources
- Database: Add Redis for sessions/cache
- CDN: Cloudflare for static content

## 📞 Support

For security issues:
- Review logs for security events
- Check rate limiting violations
- Monitor error rates
- Review access patterns

## 📄 License

© 2024 Wessel Stam. All rights reserved.

## 🙏 Acknowledgments

Built with security best practices from:
- OWASP Top 10
- CIS Security Benchmarks
- NIST Cybersecurity Framework
- Flask Security Documentation

---

**Note**: This is a security-focused web application. All security features are enabled by default. Review `SECURITY.md` for detailed information about each security feature.
