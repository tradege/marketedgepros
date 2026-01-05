from src.database import db
from src.models.trading_program import TradingProgram
from src.app import create_app
from decimal import Decimal

app = create_app()
app.app_context().push()

print("Starting program updates...")
print("=" * 80)

# 1. Delete $5K programs
print("\n1. Deleting $5K programs...")
programs_to_delete = TradingProgram.query.filter(
    TradingProgram.account_size == 5000,
    TradingProgram.type.in_(['two_phase', 'instant_funding'])
).all()

for p in programs_to_delete:
    print(f"   Deleting: {p.name} (ID: {p.id})")
    db.session.delete(p)

# 2. Update Two Phase prices
print("\n2. Updating Two Phase prices...")
price_updates = {
    10000: 99,
    15000: 149,
    25000: 249,
    50000: 399,
    100000: 599,
    200000: 999,
    400000: 1799
}

for account_size, new_price in price_updates.items():
    program = TradingProgram.query.filter_by(
        type='two_phase',
        account_size=account_size
    ).first()
    
    if program:
        old_price = program.price
        program.price = Decimal(str(new_price))
        print(f"   Updated {program.name}: ${old_price} -> ${new_price}")

# 3. Add Two Phase $300K if it doesn't exist
print("\n3. Adding Two Phase $300K...")
existing_300k = TradingProgram.query.filter_by(
    type='two_phase',
    account_size=300000
).first()

if not existing_300k:
    # Get tenant_id from an existing program
    sample_program = TradingProgram.query.first()
    
    new_program = TradingProgram(
        tenant_id=sample_program.tenant_id,
        name="Two Phase $300K",
        type="two_phase",
        description="Two-phase evaluation program for $300,000 account",
        account_size=Decimal('300000'),
        profit_target=Decimal('10.00'),
        max_daily_loss=Decimal('5.00'),
        max_total_loss=Decimal('10.00'),
        price=Decimal('1299.00'),
        profit_split=Decimal('90.00'),
        is_active=True,
        rules={
            "min_trading_days": 4,
            "max_trading_days": None,
            "platforms": ["MT4", "MT5"],
            "instruments": ["Forex", "Indices", "Commodities"]
        }
    )
    db.session.add(new_program)
    print(f"   Added: Two Phase $300K - $1,299")
else:
    print(f"   Two Phase $300K already exists (ID: {existing_300k.id})")
    existing_300k.price = Decimal('1299.00')
    print(f"   Updated price to $1,299")

# Commit all changes
print("\n4. Committing changes to database...")
try:
    db.session.commit()
    print("   ✅ All changes committed successfully!")
except Exception as e:
    db.session.rollback()
    print(f"   ❌ Error: {e}")
    raise

# Show final state
print("\n5. Final Two Phase programs:")
print("-" * 80)
two_phase_programs = TradingProgram.query.filter_by(type='two_phase').order_by(TradingProgram.account_size).all()
for p in two_phase_programs:
    print(f"   ${p.account_size:>10} - ${p.price:>8} - {p.name}")

print("=" * 80)
print("✅ Program update completed!")

