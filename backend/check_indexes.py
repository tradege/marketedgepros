from src.app import app, db

with app.app_context():
    result = db.session.execute("""
        SELECT tablename, indexname 
        FROM pg_indexes 
        WHERE tablename IN ('commissions', 'challenges', 'referrals', 'users', 'affiliate_links')
        ORDER BY tablename, indexname;
    """)
    
    print("\n=== Existing Indexes ===")
    for row in result:
        print(f"{row[0]:20} -> {row[1]}")
    print()
