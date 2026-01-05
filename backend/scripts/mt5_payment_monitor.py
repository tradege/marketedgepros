"""
MT5 Payment Monitoring Script
Monitor and validate payment-to-MT5 account creation flow
"""
import sys
sys.path.insert(0, "/var/www/MarketEdgePros/backend")

from src.database import db
from src.models.payment import Payment
from src.models.trading_program import Challenge
from src.models.mt5_models import MT5Account
from sqlalchemy import func, and_
from datetime import datetime, timedelta

def check_payment_mt5_sync():
    """Check if all paid challenges have MT5 accounts"""
    
    print("=" * 70)
    print("PAYMENT → MT5 ACCOUNT SYNC CHECK")
    print("=" * 70)
    
    # Get all paid challenges
    paid_challenges = Challenge.query.filter_by(payment_status='paid').all()
    
    print(f"\n📊 Total Paid Challenges: {len(paid_challenges)}")
    
    # Check which ones have MT5 accounts
    missing_mt5 = []
    has_mt5 = []
    
    for challenge in paid_challenges:
        mt5_account = MT5Account.query.filter_by(challenge_id=challenge.id).first()
        if mt5_account:
            has_mt5.append({
                'challenge_id': challenge.id,
                'user_id': challenge.user_id,
                'mt5_login': mt5_account.mt5_login,
                'status': mt5_account.status,
                'created_at': challenge.created_at
            })
        else:
            missing_mt5.append({
                'challenge_id': challenge.id,
                'user_id': challenge.user_id,
                'program_id': challenge.program_id,
                'payment_status': challenge.payment_status,
                'created_at': challenge.created_at
            })
    
    print(f"✅ Challenges WITH MT5 accounts: {len(has_mt5)}")
    print(f"⚠️  Challenges MISSING MT5 accounts: {len(missing_mt5)}")
    
    if has_mt5:
        print("\n" + "=" * 70)
        print("✅ CHALLENGES WITH MT5 ACCOUNTS")
        print("=" * 70)
        for item in has_mt5[:10]:  # Show first 10
            print(f"  Challenge #{item['challenge_id']} | User #{item['user_id']} | MT5: {item['mt5_login']} | Status: {item['status']}")
        if len(has_mt5) > 10:
            print(f"  ... and {len(has_mt5) - 10} more")
    
    if missing_mt5:
        print("\n" + "=" * 70)
        print("⚠️  CHALLENGES MISSING MT5 ACCOUNTS (NEED ATTENTION)")
        print("=" * 70)
        for item in missing_mt5:
            print(f"  Challenge #{item['challenge_id']} | User #{item['user_id']} | Program #{item['program_id']} | Paid: {item['created_at']}")
    
    return {
        'total_paid': len(paid_challenges),
        'with_mt5': len(has_mt5),
        'missing_mt5': len(missing_mt5),
        'missing_list': missing_mt5
    }


def check_recent_payments():
    """Check recent payments and their MT5 account status"""
    
    print("\n" + "=" * 70)
    print("RECENT PAYMENTS (Last 7 Days)")
    print("=" * 70)
    
    # Get payments from last 7 days
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_payments = Payment.query.filter(
        and_(
            Payment.created_at >= seven_days_ago,
            Payment.status == 'completed'
        )
    ).all()
    
    print(f"\n📊 Total Completed Payments (Last 7 Days): {len(recent_payments)}")
    
    for payment in recent_payments:
        # Find associated challenge
        challenge = Challenge.query.filter_by(payment_id=payment.transaction_id).first()
        if challenge:
            mt5_account = MT5Account.query.filter_by(challenge_id=challenge.id).first()
            status = "✅ MT5 Created" if mt5_account else "❌ No MT5"
            mt5_login = mt5_account.mt5_login if mt5_account else "N/A"
            print(f"  Payment #{payment.id} | ${payment.amount} | Challenge #{challenge.id} | {status} | MT5: {mt5_login}")
        else:
            print(f"  Payment #{payment.id} | ${payment.amount} | ⚠️ No Challenge Found")


def check_account_parameters():
    """Check if MT5 accounts have correct parameters based on program"""
    
    print("\n" + "=" * 70)
    print("MT5 ACCOUNT PARAMETERS VALIDATION")
    print("=" * 70)
    
    mt5_accounts = MT5Account.query.join(Challenge).all()
    
    print(f"\n📊 Total MT5 Accounts: {len(mt5_accounts)}")
    
    mismatches = []
    
    for mt5_account in mt5_accounts:
        challenge = Challenge.query.get(mt5_account.challenge_id)
        if challenge:
            # Check if balance matches
            expected_balance = challenge.initial_balance
            actual_balance = mt5_account.balance
            
            if abs(expected_balance - actual_balance) > 0.01:  # Allow small floating point difference
                mismatches.append({
                    'mt5_login': mt5_account.mt5_login,
                    'challenge_id': challenge.id,
                    'expected_balance': expected_balance,
                    'actual_balance': actual_balance
                })
    
    if mismatches:
        print(f"\n⚠️  Found {len(mismatches)} balance mismatches:")
        for item in mismatches:
            print(f"  MT5 {item['mt5_login']} | Challenge #{item['challenge_id']} | Expected: ${item['expected_balance']} | Actual: ${item['actual_balance']}")
    else:
        print("\n✅ All MT5 accounts have correct balances!")


def generate_summary_report():
    """Generate summary report"""
    
    print("\n" + "=" * 70)
    print("SUMMARY REPORT")
    print("=" * 70)
    
    # Count statistics
    total_challenges = Challenge.query.count()
    paid_challenges = Challenge.query.filter_by(payment_status='paid').count()
    pending_challenges = Challenge.query.filter_by(payment_status='pending').count()
    total_mt5_accounts = MT5Account.query.count()
    active_mt5_accounts = MT5Account.query.filter_by(status='active').count()
    
    print(f"""
📊 Overall Statistics:
   - Total Challenges: {total_challenges}
   - Paid Challenges: {paid_challenges}
   - Pending Payment: {pending_challenges}
   - Total MT5 Accounts: {total_mt5_accounts}
   - Active MT5 Accounts: {active_mt5_accounts}
   
💡 Health Check:
   - Payment→MT5 Conversion Rate: {(total_mt5_accounts / paid_challenges * 100) if paid_challenges > 0 else 0:.1f}%
   - MT5 Activation Rate: {(active_mt5_accounts / total_mt5_accounts * 100) if total_mt5_accounts > 0 else 0:.1f}%
    """)


if __name__ == "__main__":
    try:
        # Run all checks
        sync_result = check_payment_mt5_sync()
        check_recent_payments()
        check_account_parameters()
        generate_summary_report()
        
        # Exit with error code if there are missing MT5 accounts
        if sync_result['missing_mt5'] > 0:
            print(f"\n⚠️  WARNING: {sync_result['missing_mt5']} paid challenges are missing MT5 accounts!")
            print("   Run manual MT5 account creation for these challenges.")
            sys.exit(1)
        else:
            print("\n✅ All paid challenges have MT5 accounts!")
            sys.exit(0)
            
    except Exception as e:
        print(f"\n❌ Error running monitoring script: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
