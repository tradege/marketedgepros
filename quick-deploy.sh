#!/bin/bash
# Quick Deployment Script for MarketEdgePros
# Run this on your production server

set -e  # Exit on error

echo "🚀 MarketEdgePros Quick Deployment Script"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ Please run as root (sudo)${NC}"
    exit 1
fi

# Variables
PROJECT_DIR="/var/www/MarketEdgePros"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

echo -e "${YELLOW}📁 Project Directory: $PROJECT_DIR${NC}"
echo ""

# Step 1: Pull latest code
echo -e "${GREEN}Step 1: Pulling latest code from GitHub...${NC}"
cd $PROJECT_DIR
git pull origin master
echo -e "${GREEN}✅ Code updated${NC}"
echo ""

# Step 2: Backend deployment
echo -e "${GREEN}Step 2: Deploying backend...${NC}"
cd $BACKEND_DIR

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt

# Run migrations
echo "Running database migrations..."
flask db upgrade

echo -e "${GREEN}✅ Backend updated${NC}"
echo ""

# Step 3: Frontend deployment
echo -e "${GREEN}Step 3: Deploying frontend...${NC}"
cd $FRONTEND_DIR

# Install dependencies
echo "Installing Node.js dependencies..."
npm install --silent

# Build
echo "Building production bundle..."
npm run build

echo -e "${GREEN}✅ Frontend built${NC}"
echo ""

# Step 4: Restart services
echo -e "${GREEN}Step 4: Restarting services...${NC}"

# Restart backend
systemctl restart marketedgepros-backend
echo "Backend service restarted"

# Reload Nginx
systemctl reload nginx
echo "Nginx reloaded"

echo -e "${GREEN}✅ Services restarted${NC}"
echo ""

# Step 5: Verify
echo -e "${GREEN}Step 5: Verifying deployment...${NC}"

# Check backend status
if systemctl is-active --quiet marketedgepros-backend; then
    echo -e "${GREEN}✅ Backend is running${NC}"
else
    echo -e "${RED}❌ Backend is NOT running${NC}"
    systemctl status marketedgepros-backend
    exit 1
fi

# Check Nginx status
if systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✅ Nginx is running${NC}"
else
    echo -e "${RED}❌ Nginx is NOT running${NC}"
    systemctl status nginx
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo ""
echo "Next steps:"
echo "1. Test the website: https://marketedgepros.com"
echo "2. Check logs: sudo journalctl -u marketedgepros-backend -f"
echo "3. Monitor for errors"
echo ""
echo "Recent commits deployed:"
git log --oneline -5
