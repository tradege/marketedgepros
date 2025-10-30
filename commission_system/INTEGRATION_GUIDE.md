# Commission System Integration Guide

## 📋 Overview

This guide explains how to integrate the complete commission and withdrawal system into MarketEdgePros.

---

## 🗄️ Database Migration

### Step 1: Backup Database

```bash
# Create backup before migration
pg_dump -U your_user -d marketedgepros > backup_$(date +%Y%m%d).sql
```

### Step 2: Run Migration

```bash
# Connect to PostgreSQL
psql -U your_user -d marketedgepros

# Run migration script
\i /path/to/migration_commission_system.sql

# Verify tables were created
\dt

# Verify new columns in users table
\d users
```

### Step 3: Verify Migration

```sql
-- Check if all tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('commissions', 'payment_methods', 'withdrawals');

-- Should return 3 rows
```

---

## 🔧 Backend Integration

### Step 1: Add Models to Your Project

Copy `models_commission.py` content into your existing `models.py` file:

```python
# In /var/www/marketedgepros/backend/models.py

# Add these imports at the top
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey, Index
from sqlalchemy.orm import relationship

# Then add the Commission, PaymentMethod, and Withdrawal models
# (Copy from models_commission.py)

# Update your existing User model to include new fields:
class User(Base):
    # ... existing fields ...
    
    # Add these new fields
    commission_rate = Column(Float, default=20.0, nullable=False)
    paid_customers_count = Column(Integer, default=0, nullable=False)
    commission_balance = Column(Float, default=0.0, nullable=False)
    pending_commission = Column(Float, default=0.0, nullable=False)
    last_withdrawal_date = Column(DateTime, nullable=True)
    can_withdraw = Column(Boolean, default=False, nullable=False)
    
    # Add relationships
    commissions_earned = relationship('Commission', foreign_keys='Commission.affiliate_id', back_populates='affiliate')
    payment_methods = relationship('PaymentMethod', back_populates='user', cascade='all, delete-orphan')
    withdrawals = relationship('Withdrawal', foreign_keys='Withdrawal.user_id', back_populates='user')
```

### Step 2: Add Commission Logic Module

```bash
# Copy commission_logic.py to your backend
cp commission_logic.py /var/www/marketedgepros/backend/
```

Update imports in `commission_logic.py`:
```python
# Change this:
from models_commission import User, Commission

# To this:
from models import User, Commission
```

### Step 3: Register API Routes

In your main Flask app file (e.g., `app.py` or `__init__.py`):

```python
# Import the blueprint
from routes_commission import commission_bp

# Register the blueprint
app.register_blueprint(commission_bp)
```

Or copy the routes into your existing routes file:

```bash
# If you have a routes/admin.py or similar
cat routes_commission.py >> /var/www/marketedgepros/backend/routes/admin.py
```

### Step 4: Trigger Commission Calculation on Payment

In your payment success handler (Stripe webhook or NOWPayments callback):

```python
from commission_logic import process_hierarchy_commissions

# After successful payment
def handle_payment_success(customer_id, amount, order_id):
    # Your existing payment logic...
    
    # Calculate and record commissions
    process_hierarchy_commissions(db.session, customer_id, amount, order_id)
    
    # Continue with your logic...
```

Example integration with Stripe webhook:

```python
@app.route('/api/stripe/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            customer_id = session['metadata']['customer_id']
            amount = session['amount_total'] / 100  # Convert cents to dollars
            order_id = session['id']
            
            # Process commissions
            from commission_logic import process_hierarchy_commissions
            process_hierarchy_commissions(db.session, customer_id, amount, order_id)
            
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
```

---

## 🎨 Frontend Integration

### Step 1: Copy React Components

```bash
# Copy all frontend components
cp frontend/*.jsx /var/www/marketedgepros/frontend/src/pages/affiliate/
```

### Step 2: Add Routes

In your `App.jsx` or router configuration:

```jsx
import AffiliateDashboard from './pages/affiliate/AffiliateDashboard';
import PaymentMethodForm from './pages/affiliate/PaymentMethodForm';
import WithdrawalRequestForm from './pages/affiliate/WithdrawalRequestForm';
import AdminWithdrawalPanel from './pages/admin/AdminWithdrawalPanel';

// Add routes
<Route path="/affiliate/dashboard" element={<AffiliateDashboard />} />
<Route path="/affiliate/payment-method" element={<PaymentMethodForm />} />
<Route path="/affiliate/withdraw" element={<WithdrawalRequestForm />} />
<Route path="/admin/withdrawals" element={<AdminWithdrawalPanel />} />
```

### Step 3: Update Navigation

Add links to affiliate navigation menu:

```jsx
{user.role === 'affiliate' && (
  <nav>
    <Link to="/affiliate/dashboard">Dashboard</Link>
    <Link to="/affiliate/payment-method">Payment Settings</Link>
    <Link to="/affiliate/withdraw">Withdraw</Link>
  </nav>
)}

{user.role === 'super_master' && (
  <nav>
    <Link to="/admin/withdrawals">Withdrawal Requests</Link>
  </nav>
)}
```

### Step 4: Update API Client

Ensure your API client includes authentication headers:

```javascript
// In your API client or axios config
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('token')}`,
  },
});
```

---

## 🧪 Testing Checklist

### Database Tests

- [ ] All tables created successfully
- [ ] New columns added to users table
- [ ] Indexes created
- [ ] Foreign keys working

### Backend Tests

- [ ] Commission calculation works
- [ ] 10-customer threshold triggers correctly
- [ ] Payment method CRUD operations work
- [ ] Withdrawal request creation works
- [ ] Admin approval/rejection works

### Frontend Tests

- [ ] Affiliate dashboard displays stats correctly
- [ ] Payment method form saves data
- [ ] Withdrawal form validates eligibility
- [ ] Admin panel shows pending withdrawals
- [ ] All buttons and actions work

### Integration Tests

1. **Test Commission Flow:**
   - Create affiliate user
   - Affiliate refers customer
   - Customer makes payment
   - Check commission created with status='pending'
   - Customer 10 makes payment
   - Check commissions released to balance
   - Check `can_withdraw` = true

2. **Test Withdrawal Flow:**
   - Affiliate sets payment method
   - Affiliate requests withdrawal
   - Check balance deducted
   - Super Master approves
   - Super Master marks as paid
   - Check commission status updated to 'paid'

3. **Test Hierarchy Commission:**
   - Super Master → Master → Affiliate → Customer
   - Customer pays $100
   - Check all three levels receive commissions based on their rates

---

## 🔒 Security Considerations

### 1. Authentication

Ensure all API endpoints check authentication:

```python
from flask_jwt_extended import jwt_required, get_jwt_identity

@commission_bp.route('/affiliate/stats')
@jwt_required()
def get_stats():
    user_id = get_jwt_identity()
    # ...
```

### 2. Authorization

Check user roles before allowing actions:

```python
def super_master_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'super_master':
            return jsonify({'error': 'Unauthorized'}), 403
        return f(*args, **kwargs)
    return decorated
```

### 3. Input Validation

Always validate and sanitize inputs:

```python
from marshmallow import Schema, fields, validate

class WithdrawalRequestSchema(Schema):
    amount = fields.Float(required=True, validate=validate.Range(min=1))

schema = WithdrawalRequestSchema()
errors = schema.validate(request.json)
if errors:
    return jsonify({'error': errors}), 400
```

### 4. SQL Injection Prevention

Use parameterized queries (SQLAlchemy does this automatically):

```python
# Good (SQLAlchemy)
user = db.session.query(User).filter(User.id == user_id).first()

# Bad (raw SQL - avoid)
user = db.session.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

### 5. Sensitive Data

Never expose full payment details in API responses:

```python
# Mask sensitive data
'account_number': account_number[-4:] if account_number else None,
'crypto_address': address[:10] + '...' + address[-10:] if address else None,
```

---

## 📊 Monitoring and Logging

### Add Logging

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Log important events
logger.info(f"Commission created: ${amount} for affiliate {affiliate_id}")
logger.warning(f"Withdrawal request rejected: {withdrawal_id}")
logger.error(f"Failed to process commission: {str(e)}")
```

### Monitor Key Metrics

- Total commissions paid
- Pending withdrawal requests
- Average time to process withdrawals
- Commission rates by affiliate

---

## 🚀 Deployment

### Step 1: Deploy Backend

```bash
# SSH to server
ssh user@your-server

# Pull latest code
cd /var/www/marketedgepros
git pull

# Run migration
psql -U marketedgepros -d marketedgepros -f database/migration_commission_system.sql

# Restart backend
sudo systemctl restart marketedgepros
```

### Step 2: Deploy Frontend

```bash
# Build frontend
cd /var/www/marketedgepros/frontend
npm run build

# Restart nginx
sudo systemctl restart nginx
```

### Step 3: Verify Deployment

```bash
# Check backend is running
curl http://localhost:5000/api/affiliate/stats

# Check frontend is accessible
curl http://your-domain.com/affiliate/dashboard
```

---

## 📝 Configuration

### Environment Variables

Add to your `.env` file:

```bash
# Commission settings
DEFAULT_COMMISSION_RATE=20.0
MINIMUM_WITHDRAWAL_AMOUNT=50.0
WITHDRAWAL_COOLDOWN_DAYS=30
COMMISSION_THRESHOLD_CUSTOMERS=10
```

### Use in Code

```python
import os

DEFAULT_COMMISSION_RATE = float(os.getenv('DEFAULT_COMMISSION_RATE', 20.0))
MINIMUM_WITHDRAWAL = float(os.getenv('MINIMUM_WITHDRAWAL_AMOUNT', 50.0))
```

---

## 🐛 Troubleshooting

### Issue: Commissions not calculating

**Check:**
- Customer has `parent_id` set (referrer)
- Payment webhook is calling `process_hierarchy_commissions()`
- Database transaction is committed

### Issue: Can't withdraw despite reaching 10 customers

**Check:**
- `paid_customers_count` is actually >= 10
- `can_withdraw` flag is set to true
- `commission_balance` > 0
- Payment method is set

### Issue: Frontend not showing data

**Check:**
- API endpoints returning data (test with curl)
- Authentication token is valid
- CORS is configured correctly
- Browser console for errors

---

## 📞 Support

For issues or questions:
1. Check logs: `/var/log/marketedgepros/app.log`
2. Review database: `psql -U marketedgepros -d marketedgepros`
3. Test API endpoints with Postman or curl

---

## ✅ Post-Integration Checklist

- [ ] Database migration completed
- [ ] Backend models integrated
- [ ] API routes registered
- [ ] Commission calculation triggered on payment
- [ ] Frontend components added
- [ ] Routes configured
- [ ] Navigation updated
- [ ] Authentication working
- [ ] Authorization working
- [ ] All tests passing
- [ ] Deployed to production
- [ ] Monitoring configured
- [ ] Documentation updated

---

**Congratulations! Your commission system is now fully integrated!** 🎉

