.PHONY: help install dev prod docker docker-down docker-logs clean test security health

help:
	@echo "Secure Portfolio Web Application - Available Commands"
	@echo "======================================================"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install       - Install dependencies and setup environment"
	@echo "  make setup         - Run automated setup script"
	@echo ""
	@echo "Development:"
	@echo "  make dev           - Run development server"
	@echo "  make prod          - Run production server (Gunicorn)"
	@echo ""
	@echo "Docker:"
	@echo "  make docker        - Build and run with Docker Compose"
	@echo "  make docker-down   - Stop Docker containers"
	@echo "  make docker-logs   - View Docker logs"
	@echo "  make docker-build  - Build Docker image"
	@echo ""
	@echo "Testing & Security:"
	@echo "  make test          - Run tests"
	@echo "  make security      - Run security checks"
	@echo "  make health        - Check application health"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean         - Clean temporary files"
	@echo "  make update        - Update dependencies"
	@echo ""

install:
	@echo "Installing dependencies..."
	@python3 -m venv venv
	@. venv/bin/activate && pip install --upgrade pip
	@. venv/bin/activate && pip install -r requirements.txt
	@echo "✓ Dependencies installed"
	@echo "Run 'source venv/bin/activate' to activate virtual environment"

setup:
	@chmod +x setup.sh
	@./setup.sh

dev:
	@echo "Starting development server..."
	@. venv/bin/activate && python run.py

prod:
	@echo "Starting production server..."
	@. venv/bin/activate && gunicorn -c gunicorn.conf.py app:app

docker:
	@echo "Starting with Docker Compose..."
	@docker-compose up -d
	@echo "✓ Application running at http://localhost:5000"
	@echo "Run 'make docker-logs' to view logs"

docker-down:
	@docker-compose down

docker-logs:
	@docker-compose logs -f

docker-build:
	@docker build -t portfolio-webapp .

test:
	@echo "Running tests..."
	@. venv/bin/activate && python -m py_compile app.py config.py run.py gunicorn.conf.py
	@echo "✓ Python syntax checks passed"

security:
	@echo "Running security checks..."
	@. venv/bin/activate && pip install --quiet safety bandit
	@echo "Checking for vulnerable dependencies..."
	@. venv/bin/activate && safety check --file requirements.txt || true
	@echo ""
	@echo "Running static security analysis..."
	@. venv/bin/activate && bandit -r app.py config.py || true
	@echo "✓ Security scan complete"

health:
	@echo "Checking application health..."
	@curl -s http://localhost:5000/health | python -m json.tool || echo "Application not running or not accessible"

clean:
	@echo "Cleaning temporary files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	@rm -rf .pytest_cache .coverage htmlcov 2>/dev/null || true
	@echo "✓ Cleaned"

update:
	@echo "Updating dependencies..."
	@. venv/bin/activate && pip install --upgrade -r requirements.txt
	@echo "✓ Dependencies updated"
	@echo "Consider running 'make security' to check for vulnerabilities"

.DEFAULT_GOAL := help
