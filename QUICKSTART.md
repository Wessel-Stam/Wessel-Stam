# Quick Start Guide 🚀

Get your secure portfolio web application running in 5 minutes!

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- OR Docker (alternative method)

## Method 1: Automated Setup (Recommended)

### Step 1: Clone the repository
```bash
git clone https://github.com/Wessel-Stam/Wessel-Stam.git
cd Wessel-Stam
```

### Step 2: Run the setup script
```bash
chmod +x setup.sh
./setup.sh
```

The script will:
- Create a virtual environment
- Install all dependencies
- Generate a secure SECRET_KEY
- Create .env configuration file

### Step 3: Start the development server
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the server
python run.py
```

### Step 4: Access your portfolio
Open your browser to: **https://localhost:5000**

Note: You'll see a security warning about the self-signed certificate. This is normal in development. Click "Advanced" → "Proceed" to continue.

## Method 2: Docker (Even Easier!)

### Step 1: Clone the repository
```bash
git clone https://github.com/Wessel-Stam/Wessel-Stam.git
cd Wessel-Stam
```

### Step 2: Start with Docker Compose
```bash
docker-compose up -d
```

### Step 3: Access your portfolio
Open your browser to: **http://localhost:5000**

### Check status
```bash
docker-compose ps
docker-compose logs -f
```

## Method 3: Manual Setup

### Step 1: Clone and setup
```bash
git clone https://github.com/Wessel-Stam/Wessel-Stam.git
cd Wessel-Stam
```

### Step 2: Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure environment
```bash
# Copy example configuration
cp .env.example .env

# Generate secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Edit .env and paste the generated key
nano .env  # or use your preferred editor
```

### Step 5: Run the server
```bash
python run.py
```

### Step 6: Access your portfolio
**https://localhost:5000**

## Common Issues & Solutions

### Issue: Port 5000 already in use
```bash
# Check what's using the port
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use a different port
export PORT=8080
python run.py
```

### Issue: SSL certificate error
This is normal in development. The server uses a self-signed certificate.

**Solution**: Click "Advanced" → "Proceed to localhost" in your browser.

### Issue: Module not found
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Permission denied
```bash
# Make scripts executable
chmod +x setup.sh run.py
```

## What's Running?

When you start the development server:

✅ Flask web application on port 5000
✅ Self-signed HTTPS certificate
✅ Security headers enabled
✅ Rate limiting active
✅ CSRF protection enabled
✅ Session security configured
✅ Input validation active

## Next Steps

### Customize Your Portfolio
Edit these files:
- `index.html` - Your content
- `styles.css` - Your styling
- `script.js` - Interactive features

### Production Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Cloud deployment (AWS, Heroku, DigitalOcean, GCP)
- SSL/TLS certificates
- Nginx reverse proxy
- Systemd service
- Monitoring setup

### Security Features
See [SECURITY.md](SECURITY.md) for details on:
- HTTPS enforcement
- Security headers
- Rate limiting
- CSRF protection
- Session management
- Input validation

## Environment Variables

Default configuration (in `.env`):
```bash
FLASK_ENV=development
SECRET_KEY=<generated>
PORT=5000
HOST=0.0.0.0
```

## Health Check

Verify the app is running:
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{"status": "healthy", "service": "portfolio-webapp"}
```

## Stopping the Server

### Python Development Server
Press `Ctrl+C` in the terminal

### Docker
```bash
docker-compose down
```

## Production Deployment (Quick)

### Using Gunicorn
```bash
# Set production environment
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key

# Run with Gunicorn
gunicorn -c gunicorn.conf.py app:app
```

### Using Docker (Production)
```bash
# Set production secret key
export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Start
docker-compose up -d

# Production ready!
```

## Documentation

- 📖 **[WEBAPP-README.md](WEBAPP-README.md)** - Full application documentation
- 🔒 **[SECURITY.md](SECURITY.md)** - Security features and best practices
- 🚀 **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete deployment guide
- 🎨 **[PORTFOLIO-README.md](PORTFOLIO-README.md)** - Portfolio website details

## Support

Need help?
1. Check the documentation above
2. Review logs: `docker-compose logs -f` or terminal output
3. Verify environment variables in `.env`
4. Check health endpoint: `curl http://localhost:5000/health`

## Features Enabled by Default

| Feature | Status |
|---------|--------|
| HTTPS | ✅ (self-signed in dev) |
| Security Headers | ✅ |
| Rate Limiting | ✅ |
| CSRF Protection | ✅ |
| Input Validation | ✅ |
| Session Security | ✅ |
| Error Handling | ✅ |
| Logging | ✅ |
| Health Checks | ✅ |

## One-Line Installers

### Linux/macOS
```bash
git clone https://github.com/Wessel-Stam/Wessel-Stam.git && cd Wessel-Stam && chmod +x setup.sh && ./setup.sh && source venv/bin/activate && python run.py
```

### Docker
```bash
git clone https://github.com/Wessel-Stam/Wessel-Stam.git && cd Wessel-Stam && docker-compose up -d
```

## Security Notice

⚠️ **Development Mode**: The default setup runs in development mode with:
- Self-signed SSL certificate
- Debug logging enabled
- Relaxed security settings

✅ **Production Mode**: See [DEPLOYMENT.md](DEPLOYMENT.md) for production setup with:
- Valid SSL certificates
- Strict security settings
- Production-grade server (Gunicorn)

---

**Congratulations!** 🎉 Your secure portfolio web application is now running!
