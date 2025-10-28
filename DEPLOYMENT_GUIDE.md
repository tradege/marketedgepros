# PropTradePro - Deployment Guide to Production Server

**Date:** October 28, 2025  
**Version:** 1.0  
**Target Server:** 146.190.21.113 (marketedgepros.com)

---

## OVERVIEW

This guide will help you deploy the PropTradePro application to your production server with the latest fixes applied.

**Recent Changes:**
- ✅ Fixed hierarchy system (Master → Affiliate only)
- ✅ Added route aliases (/terms, /privacy)
- ✅ Comprehensive security audit completed
- ✅ All changes pushed to GitHub

---

## PREREQUISITES

### Server Requirements:
- Ubuntu 22.04 LTS or newer
- 4GB RAM minimum (8GB recommended)
- 50GB disk space
- Root or sudo access

### Software Required:
- Node.js 18+ (for frontend)
- Python 3.10+ (for backend)
- PostgreSQL 14+
- Redis 6+
- Nginx
- SSL certificate (Let's Encrypt)

---

## STEP 1: PULL LATEST CODE FROM GITHUB

```bash
# SSH into your server
ssh root@146.190.21.113

# Navigate to project directory
cd /var/www/MarketEdgePros

# Pull latest changes
git pull origin master

# Verify the changes
git log --oneline -5
```

**Expected commits:**
- `11bc1af` - Fix: Add route aliases for /terms and /privacy
- `4f2401a` - Fix: Correct hierarchy system

---

## STEP 2: ENVIRONMENT VARIABLES

### Backend Environment Variables

Create/update `/var/www/MarketEdgePros/backend/.env`:

```bash
# Application
FLASK_ENV=production
SECRET_KEY=<generate-random-64-char-string>
JWT_SECRET_KEY=<generate-random-64-char-string>

# Database
DATABASE_URL=postgresql://proptrade_user:PASSWORD@localhost:5432/proptradepro_prod

# Redis
REDIS_URL=redis://localhost:6379/0

# SendGrid (Email)
SENDGRID_API_KEY=<your-sendgrid-api-key>
SENDGRID_FROM_EMAIL=noreply@marketedgepros.com

# Stripe (Payments)
STRIPE_SECRET_KEY=<your-stripe-secret-key>
STRIPE_PUBLISHABLE_KEY=<your-stripe-publishable-key>
STRIPE_WEBHOOK_SECRET=<your-stripe-webhook-secret>

# CORS
CORS_ORIGINS=https://marketedgepros.com,https://www.marketedgepros.com

# Frontend URL (for email links)
FRONTEND_URL=https://marketedgepros.com

# File Uploads
UPLOAD_FOLDER=/var/www/MarketEdgePros/uploads
```

### Frontend Environment Variables

Create/update `/var/www/MarketEdgePros/frontend/.env.production`:

```bash
VITE_API_URL=https://api.marketedgepros.com
VITE_STRIPE_PUBLISHABLE_KEY=<your-stripe-publishable-key>
```

### Generate Secret Keys

```bash
# Generate SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"

# Generate JWT_SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## STEP 3: DATABASE SETUP

### Create Database (if not exists)

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE proptradepro_prod;
CREATE USER proptrade_user WITH PASSWORD 'YOUR_STRONG_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE proptradepro_prod TO proptrade_user;
\q
```

### Run Migrations

```bash
cd /var/www/MarketEdgePros/backend

# Activate virtual environment
source venv/bin/activate

# Run migrations
flask db upgrade

# Verify
flask db current
```

### Create Root SuperMaster User

```bash
# Run Python script to create root user
python3 << 'EOF'
from src.app import create_app
from src.database import db
from src.models.user import User

app = create_app('production')
with app.app_context():
    # Check if root supermaster exists
    root = User.query.filter_by(email='supermaster@marketedgepros.com').first()
    
    if not root:
        root = User(
            email='supermaster@marketedgepros.com',
            first_name='Super',
            last_name='Master',
            role='supermaster',
            can_create_same_role=True,  # This is the ROOT
            is_active=True,
            is_verified=True,
            level=0
        )
        root.set_password('ChangeThisPassword123!')
        root.update_tree_path()
        
        db.session.add(root)
        db.session.commit()
        
        print(f"✅ Root SuperMaster created: {root.email}")
        print(f"⚠️  CHANGE PASSWORD IMMEDIATELY!")
    else:
        print(f"✅ Root SuperMaster already exists: {root.email}")
EOF
```

**⚠️ IMPORTANT:** Change the default password immediately after first login!

---

## STEP 4: BACKEND DEPLOYMENT

### Install Dependencies

```bash
cd /var/www/MarketEdgePros/backend

# Create virtual environment (if not exists)
python3 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install gunicorn for production
pip install gunicorn
```

### Create Systemd Service

Create `/etc/systemd/system/proptradepro-backend.service`:

```ini
[Unit]
Description=PropTradePro Backend (Gunicorn)
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/MarketEdgePros/backend
Environment="PATH=/var/www/MarketEdgePros/backend/venv/bin"
Environment="FLASK_ENV=production"
ExecStart=/var/www/MarketEdgePros/backend/venv/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:8000 \
    --timeout 120 \
    --access-logfile /var/log/proptradepro/access.log \
    --error-logfile /var/log/proptradepro/error.log \
    --log-level info \
    "src.app:create_app()"

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Create Log Directory

```bash
sudo mkdir -p /var/log/proptradepro
sudo chown www-data:www-data /var/log/proptradepro
```

### Start Backend Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable proptradepro-backend

# Start service
sudo systemctl start proptradepro-backend

# Check status
sudo systemctl status proptradepro-backend

# View logs
sudo journalctl -u proptradepro-backend -f
```

---

## STEP 5: FRONTEND DEPLOYMENT

### Install Dependencies

```bash
cd /var/www/MarketEdgePros/frontend

# Install Node.js dependencies
npm install
```

### Build for Production

```bash
# Build production bundle
npm run build

# This creates /var/www/MarketEdgePros/frontend/dist
```

---

## STEP 6: NGINX CONFIGURATION

### Create Nginx Config

Create `/etc/nginx/sites-available/marketedgepros.com`:

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name marketedgepros.com www.marketedgepros.com;
    
    return 301 https://$server_name$request_uri;
}

# Main HTTPS Server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name marketedgepros.com www.marketedgepros.com;
    
    # SSL Configuration (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/marketedgepros.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/marketedgepros.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Frontend (React)
    root /var/www/MarketEdgePros/frontend/dist;
    index index.html;
    
    # Frontend Routes (SPA)
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }
    
    # File Uploads
    location /uploads/ {
        alias /var/www/MarketEdgePros/uploads/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Static Assets (with caching)
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/json application/xml+rss;
}

# API Subdomain (optional)
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name api.marketedgepros.com;
    
    ssl_certificate /etc/letsencrypt/live/marketedgepros.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/marketedgepros.com/privkey.pem;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Enable Site

```bash
# Create symlink
sudo ln -s /etc/nginx/sites-available/marketedgepros.com /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

---

## STEP 7: SSL CERTIFICATE (Let's Encrypt)

### Install Certbot

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

### Obtain Certificate

```bash
sudo certbot --nginx -d marketedgepros.com -d www.marketedgepros.com -d api.marketedgepros.com
```

### Auto-Renewal

```bash
# Test renewal
sudo certbot renew --dry-run

# Certbot automatically sets up cron job for renewal
```

---

## STEP 8: REDIS SETUP

### Install Redis

```bash
sudo apt install redis-server

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Test
redis-cli ping
# Should return: PONG
```

---

## STEP 9: VERIFY DEPLOYMENT

### Check Services

```bash
# Backend
sudo systemctl status proptradepro-backend

# Nginx
sudo systemctl status nginx

# PostgreSQL
sudo systemctl status postgresql

# Redis
sudo systemctl status redis-server
```

### Test API

```bash
# Health check
curl https://api.marketedgepros.com/api/v1/health

# Should return: {"status": "healthy"}
```

### Test Frontend

Open browser: https://marketedgepros.com

**Verify:**
- ✅ Homepage loads
- ✅ Can navigate to /programs
- ✅ Can navigate to /terms (should redirect to /terms-of-service)
- ✅ Can navigate to /privacy (should redirect to /privacy-policy)
- ✅ Can login
- ✅ Can register

---

## STEP 10: POST-DEPLOYMENT

### Monitor Logs

```bash
# Backend logs
sudo journalctl -u proptradepro-backend -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Application logs
sudo tail -f /var/log/proptradepro/error.log
```

### Create Backups

```bash
# Database backup script
cat > /root/backup-db.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U proptrade_user proptradepro_prod | gzip > /backups/db_$DATE.sql.gz
# Keep only last 7 days
find /backups -name "db_*.sql.gz" -mtime +7 -delete
EOF

chmod +x /root/backup-db.sh

# Add to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /root/backup-db.sh") | crontab -
```

### Setup Monitoring (Optional)

```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Consider setting up:
# - Sentry (error tracking)
# - Datadog/New Relic (APM)
# - Uptime monitoring (Pingdom, UptimeRobot)
```

---

## TROUBLESHOOTING

### Backend Won't Start

```bash
# Check logs
sudo journalctl -u proptradepro-backend -n 50

# Common issues:
# 1. Database connection - check DATABASE_URL
# 2. Missing dependencies - pip install -r requirements.txt
# 3. Port already in use - sudo lsof -i :8000
```

### Frontend Not Loading

```bash
# Check Nginx
sudo nginx -t
sudo systemctl status nginx

# Rebuild frontend
cd /var/www/MarketEdgePros/frontend
npm run build
```

### Database Connection Error

```bash
# Check PostgreSQL
sudo systemctl status postgresql

# Test connection
psql -U proptrade_user -d proptradepro_prod -h localhost

# Check .env file
cat /var/www/MarketEdgePros/backend/.env | grep DATABASE_URL
```

---

## ROLLBACK PROCEDURE

If something goes wrong:

```bash
# 1. Revert Git changes
cd /var/www/MarketEdgePros
git log --oneline -10
git revert <commit-hash>

# 2. Rebuild
cd frontend && npm run build

# 3. Restart backend
sudo systemctl restart proptradepro-backend

# 4. Check status
sudo systemctl status proptradepro-backend
```

---

## SECURITY CHECKLIST

- [ ] All environment variables set
- [ ] Strong passwords used
- [ ] SSL certificate installed
- [ ] Firewall configured (ufw)
- [ ] SSH key authentication enabled
- [ ] Root login disabled
- [ ] Database backups scheduled
- [ ] Monitoring set up
- [ ] Error tracking configured
- [ ] Rate limiting enabled

---

## NEXT STEPS

After successful deployment:

1. **Change default SuperMaster password**
2. **Test all user roles** (SuperMaster, Master, Affiliate, Trader)
3. **Test payment flow** with Stripe test mode
4. **Test email system** with SendGrid
5. **Monitor logs** for first 24 hours
6. **Run security scan** (optional)
7. **Load testing** (optional)

---

## SUPPORT

If you encounter issues:

1. Check logs first
2. Review this guide
3. Check GitHub issues
4. Contact Manus AI for assistance

---

**Deployment Guide Version:** 1.0  
**Last Updated:** October 28, 2025  
**Prepared by:** Manus AI

---

**Good luck with your deployment! 🚀**

