# Environment Variables Checklist

**Server:** 146.190.21.113 (marketedgepros.com)  
**Date:** October 28, 2025

---

## BACKEND ENVIRONMENT VARIABLES

File: `/var/www/MarketEdgePros/backend/.env`

### Required (Critical):

```bash
# Application
FLASK_ENV=production
SECRET_KEY=<GENERATE_64_CHAR_RANDOM_STRING>
JWT_SECRET_KEY=<GENERATE_64_CHAR_RANDOM_STRING>

# Database
DATABASE_URL=postgresql://proptrade_user:PASSWORD@localhost:5432/proptradepro_prod

# Redis
REDIS_URL=redis://localhost:6379/0

# SendGrid (Email)
SENDGRID_API_KEY=<YOUR_SENDGRID_API_KEY>
SENDGRID_FROM_EMAIL=noreply@marketedgepros.com

# Stripe (Payments)
STRIPE_SECRET_KEY=<YOUR_STRIPE_SECRET_KEY>
STRIPE_PUBLISHABLE_KEY=<YOUR_STRIPE_PUBLISHABLE_KEY>
STRIPE_WEBHOOK_SECRET=<YOUR_STRIPE_WEBHOOK_SECRET>
```

### Optional (Recommended):

```bash
# CORS
CORS_ORIGINS=https://marketedgepros.com,https://www.marketedgepros.com

# Frontend URL (for email links)
FRONTEND_URL=https://marketedgepros.com

# File Uploads
UPLOAD_FOLDER=/var/www/MarketEdgePros/uploads

# MetaTrader (if using)
MT_SERVER=<YOUR_MT_SERVER>
MT_LOGIN=<YOUR_MT_LOGIN>
MT_PASSWORD=<YOUR_MT_PASSWORD>
```

---

## FRONTEND ENVIRONMENT VARIABLES

File: `/var/www/MarketEdgePros/frontend/.env.production`

```bash
VITE_API_URL=https://api.marketedgepros.com
VITE_STRIPE_PUBLISHABLE_KEY=<YOUR_STRIPE_PUBLISHABLE_KEY>
```

---

## HOW TO GENERATE SECRET KEYS

### Method 1: Python

```bash
# SECRET_KEY (64 characters)
python3 -c "import secrets; print(secrets.token_hex(32))"

# JWT_SECRET_KEY (64 characters)
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### Method 2: OpenSSL

```bash
openssl rand -hex 32
```

### Method 3: Online Generator

Use: https://randomkeygen.com/ (CodeIgniter Encryption Keys)

---

## EXTERNAL SERVICES SETUP

### 1. SendGrid (Email Service)

**Website:** https://sendgrid.com

**Steps:**
1. Create account
2. Verify domain (marketedgepros.com)
3. Create API Key
4. Set `SENDGRID_API_KEY` in .env
5. Set `SENDGRID_FROM_EMAIL` to verified email

**Test:**
```bash
curl --request POST \
  --url https://api.sendgrid.com/v3/mail/send \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"personalizations":[{"to":[{"email":"test@example.com"}]}],"from":{"email":"noreply@marketedgepros.com"},"subject":"Test","content":[{"type":"text/plain","value":"Test"}]}'
```

---

### 2. Stripe (Payment Processing)

**Website:** https://stripe.com

**Steps:**
1. Create account
2. Get API keys (Dashboard → Developers → API keys)
3. Set up webhook endpoint: `https://api.marketedgepros.com/api/v1/payments/webhook`
4. Get webhook secret
5. Set all 3 keys in .env

**Test Mode Keys:**
- Use test keys for development
- Switch to live keys for production

**Webhook Events to Listen:**
- `payment_intent.succeeded`
- `payment_intent.payment_failed`
- `customer.subscription.created`
- `customer.subscription.deleted`

---

### 3. PostgreSQL Database

**Setup:**
```bash
sudo -u postgres psql

CREATE DATABASE proptradepro_prod;
CREATE USER proptrade_user WITH PASSWORD 'STRONG_PASSWORD_HERE';
GRANT ALL PRIVILEGES ON DATABASE proptradepro_prod TO proptrade_user;
\q
```

**Connection String:**
```
postgresql://proptrade_user:PASSWORD@localhost:5432/proptradepro_prod
```

---

### 4. Redis

**Install:**
```bash
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

**Test:**
```bash
redis-cli ping
# Should return: PONG
```

**Connection String:**
```
redis://localhost:6379/0
```

---

## VERIFICATION CHECKLIST

### Before Deployment:

- [ ] All SECRET_KEY values are unique and random
- [ ] Database credentials are strong
- [ ] SendGrid API key is valid
- [ ] Stripe keys are correct (test or live)
- [ ] CORS_ORIGINS includes your domain
- [ ] FRONTEND_URL is correct (for email links)
- [ ] All .env files are NOT committed to Git

### After Deployment:

- [ ] Backend can connect to database
- [ ] Backend can connect to Redis
- [ ] Emails are being sent (check SendGrid dashboard)
- [ ] Payments work (test with Stripe test cards)
- [ ] CORS is working (no browser errors)
- [ ] File uploads work

---

## SECURITY NOTES

### ⚠️ NEVER:
- Commit .env files to Git
- Share API keys publicly
- Use weak passwords
- Use development keys in production
- Expose database ports publicly

### ✅ ALWAYS:
- Use strong, random secret keys
- Rotate keys periodically
- Use environment variables (never hardcode)
- Enable 2FA on all external services
- Monitor API usage and logs
- Set up alerts for suspicious activity

---

## STRIPE TEST CARDS

For testing payments:

**Success:**
- Card: 4242 4242 4242 4242
- Expiry: Any future date
- CVC: Any 3 digits

**Decline:**
- Card: 4000 0000 0000 0002

**More:** https://stripe.com/docs/testing

---

## SENDGRID TESTING

**Test Email Sending:**
```bash
# From backend directory
python3 << 'EOF'
from src.app import create_app
from src.services.email_service import EmailService

app = create_app('production')
with app.app_context():
    # Create a test user object
    class TestUser:
        email = 'your-email@example.com'
        first_name = 'Test'
    
    user = TestUser()
    result = EmailService.send_verification_email(user, '123456')
    print(f"Email sent: {result}")
EOF
```

---

## TROUBLESHOOTING

### "Database connection failed"
- Check DATABASE_URL format
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Test connection: `psql -U proptrade_user -d proptradepro_prod -h localhost`

### "SendGrid API error"
- Verify API key is correct
- Check SendGrid dashboard for errors
- Ensure sender email is verified

### "Stripe webhook failed"
- Check webhook secret matches
- Verify webhook URL is accessible
- Check Stripe dashboard → Webhooks → Logs

### "Redis connection refused"
- Check Redis is running: `sudo systemctl status redis-server`
- Test connection: `redis-cli ping`

---

## QUICK REFERENCE

### Generate All Keys at Once:

```bash
echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
echo "JWT_SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
```

### Copy .env Template:

```bash
# Backend
cp /var/www/MarketEdgePros/backend/.env.example /var/www/MarketEdgePros/backend/.env

# Frontend
cp /var/www/MarketEdgePros/frontend/.env.example /var/www/MarketEdgePros/frontend/.env.production
```

### Edit .env Files:

```bash
# Backend
nano /var/www/MarketEdgePros/backend/.env

# Frontend
nano /var/www/MarketEdgePros/frontend/.env.production
```

---

**Last Updated:** October 28, 2025  
**Prepared by:** Manus AI

