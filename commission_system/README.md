# MarketEdgePros Commission System

Complete commission and withdrawal management system for prop trading firm platform.

## 📦 Package Contents

### Backend
- `backend/models_commission.py` - Database models (User extensions, Commission, PaymentMethod, Withdrawal)
- `backend/commission_logic.py` - Business logic for commission calculation and tracking
- `backend/routes_commission.py` - Flask API routes (15 endpoints)

### Frontend
- `frontend/AffiliateDashboard.jsx` - Affiliate dashboard with stats and progress
- `frontend/PaymentMethodForm.jsx` - Payment method setup form
- `frontend/WithdrawalRequestForm.jsx` - Withdrawal request interface
- `frontend/AdminWithdrawalPanel.jsx` - Super Master withdrawal approval panel

### Database
- `database/migration_commission_system.sql` - Complete database migration script

### Documentation
- `INTEGRATION_GUIDE.md` - Step-by-step integration instructions
- `README.md` - This file

## 🎯 Features

### For Affiliates
- ✅ Real-time commission tracking
- ✅ Progress bar to 10-customer threshold
- ✅ Automatic commission release at 10 customers
- ✅ Multiple payment methods (Bank, PayPal, Crypto, Wise)
- ✅ Withdrawal request system
- ✅ Commission history and statistics
- ✅ Customer list and tracking

### For Super Master (Admin)
- ✅ Withdrawal approval workflow
- ✅ View all pending/approved/paid/rejected withdrawals
- ✅ User payment details visibility
- ✅ Approve/reject with notes
- ✅ Mark as paid functionality

### System Features
- ✅ Hierarchical commission calculation (Super Master → Master → Affiliate)
- ✅ 10-customer threshold before withdrawal eligibility
- ✅ 30-day cooldown between withdrawals
- ✅ Automatic commission calculation on payment
- ✅ Secure payment detail storage
- ✅ Complete audit trail

## 🚀 Quick Start

1. **Run Database Migration**
   ```bash
   psql -U your_user -d marketedgepros -f database/migration_commission_system.sql
   ```

2. **Integrate Backend**
   - Copy models to your `models.py`
   - Add `commission_logic.py` to your backend
   - Register routes from `routes_commission.py`

3. **Integrate Frontend**
   - Copy React components to your frontend
   - Add routes to your router
   - Update navigation menu

4. **Trigger Commission Calculation**
   ```python
   from commission_logic import process_hierarchy_commissions
   
   # In your payment success handler
   process_hierarchy_commissions(db.session, customer_id, amount, order_id)
   ```

5. **Test the System**
   - Create affiliate account
   - Refer customers
   - Make test payments
   - Verify commissions calculated
   - Test withdrawal flow

## 📊 Database Schema

### New Tables
- `commissions` - Commission records
- `payment_methods` - User payment details
- `withdrawals` - Withdrawal requests

### User Table Extensions
- `commission_rate` - Percentage commission (default 20%)
- `paid_customers_count` - Number of paying customers
- `commission_balance` - Available for withdrawal
- `pending_commission` - Locked until 10 customers
- `last_withdrawal_date` - Last withdrawal timestamp
- `can_withdraw` - Eligibility flag

## 🔐 Security

- ✅ Authentication required for all endpoints
- ✅ Role-based access control
- ✅ Input validation and sanitization
- ✅ Sensitive data masking
- ✅ SQL injection prevention (SQLAlchemy)
- ✅ Transaction safety

## 📖 API Endpoints

### Affiliate Endpoints
- `GET /api/affiliate/stats` - Get commission statistics
- `GET /api/affiliate/commissions` - List commissions (paginated)
- `GET /api/affiliate/customers` - List referred customers
- `GET /api/payment-method` - Get active payment method
- `POST /api/payment-method` - Create/update payment method
- `GET /api/withdrawal/eligibility` - Check withdrawal eligibility
- `POST /api/withdrawal/request` - Request withdrawal
- `GET /api/withdrawal/history` - Get withdrawal history

### Admin Endpoints
- `GET /api/admin/withdrawals/pending` - Get pending withdrawals
- `POST /api/admin/withdrawals/:id/approve` - Approve withdrawal
- `POST /api/admin/withdrawals/:id/mark-paid` - Mark as paid
- `POST /api/admin/withdrawals/:id/reject` - Reject withdrawal

## 🎨 UI Components

All components use Tailwind CSS and are fully responsive.

### AffiliateDashboard
- Progress cards (customers, pending, balance, total)
- Action buttons (withdraw, payment settings, customers)
- Recent commissions table

### PaymentMethodForm
- Method type selection (Bank, PayPal, Crypto, Wise)
- Conditional fields based on method
- Validation and error handling

### WithdrawalRequestForm
- Balance display
- Amount input with validation
- Eligibility checking
- Withdrawal history table

### AdminWithdrawalPanel
- Tabbed interface (Pending, Approved, Paid, Rejected)
- User and payment details
- Approve/reject actions
- Rejection reason modal

## 🧪 Testing

See `INTEGRATION_GUIDE.md` for complete testing checklist.

## 📝 Configuration

Environment variables:
```bash
DEFAULT_COMMISSION_RATE=20.0
MINIMUM_WITHDRAWAL_AMOUNT=50.0
WITHDRAWAL_COOLDOWN_DAYS=30
COMMISSION_THRESHOLD_CUSTOMERS=10
```

## 🤝 Support

For integration help, refer to `INTEGRATION_GUIDE.md`.

## 📄 License

Proprietary - MarketEdgePros

---

**Built with ❤️ for MarketEdgePros**
