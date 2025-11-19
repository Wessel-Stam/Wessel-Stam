#!/bin/bash
# Setup script for Secure Portfolio Web Application
# Author: Wessel Stam

set -e

echo "=================================="
echo "Portfolio Web App Setup"
echo "=================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.11 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}Found Python $PYTHON_VERSION${NC}"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists. Skipping.${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}Virtual environment created${NC}"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Setup environment file
echo ""
if [ -f ".env" ]; then
    echo -e "${YELLOW}.env file already exists. Skipping creation.${NC}"
else
    echo "Creating .env file..."
    cp .env.example .env
    
    # Generate secret key
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    
    # Update .env with generated secret key
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/your-secret-key-here-generate-with-python-secrets/$SECRET_KEY/" .env
    else
        # Linux
        sed -i "s/your-secret-key-here-generate-with-python-secrets/$SECRET_KEY/" .env
    fi
    
    echo -e "${GREEN}.env file created with generated SECRET_KEY${NC}"
fi

# Make run script executable
chmod +x run.py

echo ""
echo -e "${GREEN}=================================="
echo "Setup completed successfully!"
echo "==================================${NC}"
echo ""
echo "Next steps:"
echo "1. Review and update .env file if needed"
echo "2. Run the development server:"
echo "   ${YELLOW}python run.py${NC}"
echo ""
echo "3. Or run with Docker:"
echo "   ${YELLOW}docker-compose up${NC}"
echo ""
echo "Access the application at: ${GREEN}https://localhost:5000${NC}"
echo ""
echo "For production deployment, see DEPLOYMENT.md"
echo "For security features, see SECURITY.md"
echo ""
