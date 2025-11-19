# Deployment Guide

## Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Docker (optional, for containerized deployment)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Wessel-Stam/Wessel-Stam.git
   cd Wessel-Stam
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and set your SECRET_KEY
   ```

5. **Generate a secure secret key**
   ```bash
   python -c "import secrets; print(f'SECRET_KEY={secrets.token_hex(32)}')" >> .env
   ```

6. **Run the development server**
   ```bash
   python run.py
   ```

7. **Access the application**
   - Open browser to: `https://localhost:5000`
   - Note: You'll see a security warning for the self-signed certificate (this is normal in development)

## Production Deployment

### Option 1: Docker Deployment (Recommended)

1. **Build and run with Docker Compose**
   ```bash
   # Set your secret key
   export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
   
   # Build and start
   docker-compose up -d
   
   # Check status
   docker-compose ps
   
   # View logs
   docker-compose logs -f
   ```

2. **Verify deployment**
   ```bash
   curl http://localhost:5000/health
   ```

### Option 2: Direct Gunicorn Deployment

1. **Prepare environment**
   ```bash
   # Create production environment
   export FLASK_ENV=production
   export SECRET_KEY=your-production-secret-key
   export PORT=5000
   ```

2. **Run with Gunicorn**
   ```bash
   gunicorn -c gunicorn.conf.py app:app
   ```

### Option 3: Systemd Service

1. **Create service file** (`/etc/systemd/system/portfolio.service`):
   ```ini
   [Unit]
   Description=Portfolio Web Application
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/portfolio
   Environment="PATH=/var/www/portfolio/venv/bin"
   Environment="FLASK_ENV=production"
   EnvironmentFile=/var/www/portfolio/.env
   ExecStart=/var/www/portfolio/venv/bin/gunicorn -c gunicorn.conf.py app:app
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

2. **Enable and start service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable portfolio
   sudo systemctl start portfolio
   sudo systemctl status portfolio
   ```

## Nginx Reverse Proxy Setup

### Basic Configuration

1. **Install Nginx**
   ```bash
   sudo apt update
   sudo apt install nginx
   ```

2. **Create Nginx configuration** (`/etc/nginx/sites-available/portfolio`):
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com www.yourdomain.com;
       
       # Redirect to HTTPS
       return 301 https://$server_name$request_uri;
   }

   server {
       listen 443 ssl http2;
       server_name yourdomain.com www.yourdomain.com;

       # SSL Configuration
       ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_ciphers HIGH:!aNULL:!MD5;
       ssl_prefer_server_ciphers on;
       ssl_session_cache shared:SSL:10m;
       ssl_session_timeout 10m;

       # Security Headers (additional layer)
       add_header X-Frame-Options "DENY" always;
       add_header X-Content-Type-Options "nosniff" always;
       add_header X-XSS-Protection "1; mode=block" always;

       # Proxy to Flask application
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           
           # Timeouts
           proxy_connect_timeout 60s;
           proxy_send_timeout 60s;
           proxy_read_timeout 60s;
       }

       # Health check
       location /health {
           proxy_pass http://127.0.0.1:5000/health;
           access_log off;
       }

       # Rate limiting
       limit_req_zone $binary_remote_addr zone=app_limit:10m rate=10r/s;
       limit_req zone=app_limit burst=20 nodelay;
   }
   ```

3. **Enable configuration**
   ```bash
   sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### SSL/TLS with Let's Encrypt

1. **Install Certbot**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

2. **Obtain certificate**
   ```bash
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

3. **Auto-renewal**
   ```bash
   sudo certbot renew --dry-run
   ```

## Cloud Platform Deployment

### AWS EC2

1. **Launch EC2 instance**
   - Ubuntu 22.04 LTS
   - t2.micro or larger
   - Security group: Allow ports 80, 443, 22

2. **Connect and setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and dependencies
   sudo apt install python3-pip python3-venv nginx -y
   
   # Clone and setup application
   git clone https://github.com/Wessel-Stam/Wessel-Stam.git
   cd Wessel-Stam
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
   # Configure and start
   # Follow systemd service setup above
   ```

### Heroku

1. **Create Procfile**
   ```
   web: gunicorn -c gunicorn.conf.py app:app
   ```

2. **Deploy**
   ```bash
   heroku create your-app-name
   heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
   heroku config:set FLASK_ENV=production
   git push heroku main
   ```

### DigitalOcean App Platform

1. **Create app.yaml**
   ```yaml
   name: portfolio-webapp
   services:
   - name: web
     github:
       repo: Wessel-Stam/Wessel-Stam
       branch: main
       deploy_on_push: true
     run_command: gunicorn -c gunicorn.conf.py app:app
     environment_slug: python
     instance_size_slug: basic-xxs
     envs:
     - key: FLASK_ENV
       value: production
     - key: SECRET_KEY
       value: ${SECRET_KEY}
       type: SECRET
   ```

2. **Deploy**
   ```bash
   doctl apps create --spec app.yaml
   ```

### Google Cloud Run

1. **Build and push container**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/portfolio-webapp
   ```

2. **Deploy**
   ```bash
   gcloud run deploy portfolio-webapp \
     --image gcr.io/PROJECT_ID/portfolio-webapp \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars FLASK_ENV=production,SECRET_KEY=your-secret-key
   ```

## Monitoring & Maintenance

### Health Checks
```bash
# Check application health
curl http://localhost:5000/health

# Check with full headers
curl -I http://localhost:5000/
```

### Log Monitoring
```bash
# Docker logs
docker-compose logs -f webapp

# Systemd logs
sudo journalctl -u portfolio -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Performance Monitoring
```bash
# Check resource usage
docker stats portfolio-webapp

# System resources
htop
```

### Backup Strategy
```bash
# Backup configuration
tar -czf portfolio-backup-$(date +%Y%m%d).tar.gz .env *.py *.html *.css *.js

# Restore
tar -xzf portfolio-backup-YYYYMMDD.tar.gz
```

## Scaling Considerations

### Horizontal Scaling
- Use multiple Gunicorn workers
- Deploy multiple instances behind load balancer
- Configure session storage (Redis) for session sharing

### Vertical Scaling
- Increase instance size
- Adjust Gunicorn worker count
- Optimize memory settings

### Load Balancing
```nginx
upstream portfolio_backend {
    least_conn;
    server 127.0.0.1:5000 weight=1 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:5001 weight=1 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:5002 weight=1 max_fails=3 fail_timeout=30s;
}

server {
    location / {
        proxy_pass http://portfolio_backend;
    }
}
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   lsof -i :5000
   kill -9 PID
   ```

2. **Permission denied**
   ```bash
   chmod +x run.py
   sudo chown -R $USER:$USER /path/to/app
   ```

3. **Module not found**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

4. **SSL certificate errors**
   ```bash
   pip install pyopenssl --upgrade
   ```

5. **Rate limit errors**
   - Increase limits in app.py
   - Use Redis for distributed rate limiting

### Debug Mode
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python run.py
```

## Security Checklist

Before going to production:
- [ ] Set strong SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Test rate limiting
- [ ] Review security headers
- [ ] Update all dependencies
- [ ] Test error handling
- [ ] Configure logging
- [ ] Set up alerts
- [ ] Document incident response plan

## Support

For issues or questions:
- Check logs: Application, Nginx, System
- Review SECURITY.md for security features
- Test health endpoint: `/health`
- Verify environment variables
