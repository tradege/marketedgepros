from src.database import db
from src.models.trading_program import TradingProgram
from src.app import create_app

app = create_app()
app.app_context().push()

programs = TradingProgram.query.order_by(TradingProgram.account_size).all()
print("Current Programs:")
print("-" * 80)
for p in programs:
    print(f'ID: {p.id} | {p.name} | ${p.account_size} | Price: ${p.price} | Type: {p.type}')
print("-" * 80)
print(f"Total programs: {len(programs)}")

