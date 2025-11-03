from src.database import db
from src.models.trading_program import TradingProgram, ProgramAddOn
from src.app import create_app
from decimal import Decimal

app = create_app()
app.app_context().push()

print("Creating Add-ons for all Two Phase programs...")
print("=" * 80)

# Define add-ons
addons_config = [
    {
        'name': 'Increased Leverage',
        'description': 'Trade with higher leverage for greater profit potential',
        'price': Decimal('75.00'),
        'price_type': 'fixed',
        'benefits': {
            'leverage': '1:100',
            'description': 'Increase your leverage from 1:30 to 1:100'
        }
    },
    {
        'name': '90% Profit Split',
        'description': 'Keep 90% of your profits instead of 80%',
        'price': Decimal('100.00'),
        'price_type': 'fixed',
        'benefits': {
            'profit_split': '90%',
            'description': 'Earn an extra 10% on all your profits'
        }
    },
    {
        'name': 'Bi-weekly Payouts',
        'description': 'Get paid every 2 weeks instead of monthly',
        'price': Decimal('50.00'),
        'price_type': 'fixed',
        'benefits': {
            'payout_frequency': 'Bi-weekly',
            'description': 'Receive your profits twice as often'
        }
    },
    {
        'name': 'No Minimum Trading Days',
        'description': 'Remove the minimum trading days requirement',
        'price': Decimal('30.00'),
        'price_type': 'fixed',
        'benefits': {
            'min_days': '0',
            'description': 'Trade whenever you want, no minimum days required'
        }
    }
]

# Get all Two Phase programs
two_phase_programs = TradingProgram.query.filter_by(type='two_phase').all()

print(f"\nFound {len(two_phase_programs)} Two Phase programs")
print("-" * 80)

for program in two_phase_programs:
    print(f"\nAdding add-ons to: {program.name} (${program.account_size})")
    
    # Check if add-ons already exist
    existing_addons = ProgramAddOn.query.filter_by(program_id=program.id).count()
    
    if existing_addons > 0:
        print(f"  ⚠️  {existing_addons} add-ons already exist, skipping...")
        continue
    
    # Create add-ons for this program
    for addon_config in addons_config:
        addon = ProgramAddOn(
            program_id=program.id,
            name=addon_config['name'],
            description=addon_config['description'],
            price=addon_config['price'],
            price_type=addon_config['price_type'],
            benefits=addon_config['benefits'],
            is_active=True
        )
        db.session.add(addon)
        print(f"  ✅ Added: {addon_config['name']} (+${addon_config['price']})")

# Commit all changes
print("\n" + "=" * 80)
print("Committing changes to database...")
try:
    db.session.commit()
    print("✅ All add-ons created successfully!")
except Exception as e:
    db.session.rollback()
    print(f"❌ Error: {e}")
    raise

# Show summary
print("\n" + "=" * 80)
print("Summary:")
print("-" * 80)

for program in two_phase_programs:
    addons = ProgramAddOn.query.filter_by(program_id=program.id).all()
    print(f"\n{program.name}:")
    for addon in addons:
        print(f"  - {addon.name}: ${addon.price}")

print("\n" + "=" * 80)
print("✅ Add-ons creation completed!")

