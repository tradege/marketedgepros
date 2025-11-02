"""
Analyze test coverage and identify gaps
"""

# Coverage data from pytest output
coverage_data = {
    # Services (Critical - Business Logic)
    "services": [
        ("auth_service.py", 74, "HIGH", "Authentication - already good coverage"),
        ("email_service_async.py", 80, "MEDIUM", "Async emails - good coverage"),
        ("email_service.py", 51, "HIGH", "Email sending - needs more tests"),
        ("notification_service.py", 51, "MEDIUM", "Notifications - needs tests"),
        ("analytics_service.py", 29, "HIGH", "Analytics - critical, needs tests"),
        ("discord_service.py", 25, "LOW", "Discord - already has test_discord.py"),
        ("payment_approval_service.py", 23, "HIGH", "Payment approvals - critical"),
        ("wallet_service.py", 21, "HIGH", "Wallet operations - critical"),
        ("storage_service.py", 20, "MEDIUM", "File storage - needs tests"),
        ("openai_service.py", 19, "LOW", "AI features - optional"),
        ("payment_service.py", 16, "CRITICAL", "Payments - MUST have tests"),
        ("commission_service.py", 13, "CRITICAL", "Commissions - MUST have tests"),
        ("file_service.py", 27, "MEDIUM", "File uploads - needs tests"),
    ],
    
    # Routes (API Endpoints)
    "routes": [
        ("auth.py", 35, "HIGH", "Auth endpoints - partially tested"),
        ("admin.py", 33, "HIGH", "Admin panel - needs tests"),
        ("wallet.py", 34, "HIGH", "Wallet API - needs tests"),
        ("users.py", 35, "MEDIUM", "User management"),
        ("traders.py", 30, "MEDIUM", "Trader management"),
        ("uploads.py", 30, "MEDIUM", "File uploads"),
        ("challenges.py", 33, "HIGH", "Challenge management"),
        ("commissions.py", 25, "HIGH", "Commission routes"),
        ("payments.py", 25, "HIGH", "Payment routes"),
        ("support/tickets.py", 25, "MEDIUM", "Support system"),
        ("support/articles.py", 24, "LOW", "Knowledge base"),
    ],
    
    # Models (Data Layer)
    "models": [
        ("user.py", 50, "HIGH", "User model - core entity"),
        ("trading_program.py", 62, "MEDIUM", "Trading programs"),
        ("notification.py", 57, "MEDIUM", "Notifications"),
        ("lead.py", 51, "LOW", "Lead management"),
        ("blog_post.py", 49, "LOW", "Blog system"),
    ],
    
    # Utils (Helper Functions)
    "utils": [
        ("input_validation.py", 86, "GOOD", "Already well tested"),
        ("email_templates.py", 84, "GOOD", "Already well tested"),
        ("decorators.py", 47, "MEDIUM", "Auth decorators - needs tests"),
        ("permissions.py", 32, "HIGH", "Permission system - critical"),
        ("hierarchy_scoping.py", 30, "HIGH", "Hierarchy - critical for MLM"),
        ("validators.py", 28, "MEDIUM", "Input validators"),
        ("error_messages.py", 25, "LOW", "Error messages"),
    ],
    
    # Tasks (Background Jobs)
    "tasks": [
        ("email_tasks.py", 39, "HIGH", "Email queue - needs tests"),
        ("course_drip_campaign.py", 14, "MEDIUM", "Drip campaigns"),
    ],
}

# Priority levels
CRITICAL = []
HIGH = []
MEDIUM = []
LOW = []
GOOD = []

for category, items in coverage_data.items():
    for filename, coverage, priority, description in items:
        item = {
            "category": category,
            "file": filename,
            "coverage": coverage,
            "description": description,
            "full_path": f"src/{category}/{filename}"
        }
        
        if priority == "CRITICAL":
            CRITICAL.append(item)
        elif priority == "HIGH":
            HIGH.append(item)
        elif priority == "MEDIUM":
            MEDIUM.append(item)
        elif priority == "LOW":
            LOW.append(item)
        else:
            GOOD.append(item)

# Print analysis
print("=" * 80)
print("📊 COVERAGE ANALYSIS - WHAT NEEDS TESTS")
print("=" * 80)

print("\n🔴 CRITICAL - MUST ADD TESTS (< 20% coverage)")
print("-" * 80)
for item in sorted(CRITICAL, key=lambda x: x['coverage']):
    print(f"  {item['coverage']:3d}% | {item['file']:40s} | {item['description']}")

print("\n🟠 HIGH PRIORITY (20-50% coverage)")
print("-" * 80)
for item in sorted(HIGH, key=lambda x: x['coverage']):
    print(f"  {item['coverage']:3d}% | {item['file']:40s} | {item['description']}")

print("\n🟡 MEDIUM PRIORITY (50-70% coverage)")
print("-" * 80)
for item in sorted(MEDIUM, key=lambda x: x['coverage']):
    print(f"  {item['coverage']:3d}% | {item['file']:40s} | {item['description']}")

print("\n🟢 LOW PRIORITY (Already decent coverage)")
print("-" * 80)
for item in sorted(LOW, key=lambda x: x['coverage']):
    print(f"  {item['coverage']:3d}% | {item['file']:40s} | {item['description']}")

print("\n✅ GOOD (> 80% coverage - maintain)")
print("-" * 80)
for item in sorted(GOOD, key=lambda x: x['coverage'], reverse=True):
    print(f"  {item['coverage']:3d}% | {item['file']:40s} | {item['description']}")

# Summary
print("\n" + "=" * 80)
print("📈 SUMMARY")
print("=" * 80)
print(f"  🔴 CRITICAL:  {len(CRITICAL):2d} files - MUST add tests immediately")
print(f"  🟠 HIGH:      {len(HIGH):2d} files - Should add tests soon")
print(f"  🟡 MEDIUM:    {len(MEDIUM):2d} files - Add tests when possible")
print(f"  🟢 LOW:       {len(LOW):2d} files - Already decent")
print(f"  ✅ GOOD:      {len(GOOD):2d} files - Well tested")
print(f"  📊 TOTAL:     {len(CRITICAL) + len(HIGH) + len(MEDIUM) + len(LOW) + len(GOOD):2d} files analyzed")

print("\n" + "=" * 80)
print("🎯 RECOMMENDED ACTION PLAN")
print("=" * 80)
print("\n1. WEEK 1 - Critical Services (Payment & Commission)")
print("   - test_payment_service.py")
print("   - test_commission_service.py")
print("   - test_wallet_service.py")
print("\n2. WEEK 2 - High Priority (Auth & Admin)")
print("   - test_payment_approval_service.py")
print("   - test_analytics_service.py")
print("   - test_admin_routes.py")
print("\n3. WEEK 3 - Medium Priority (Supporting Features)")
print("   - test_email_tasks.py")
print("   - test_file_service.py")
print("   - test_permissions.py")
print("\n4. WEEK 4 - Polish & Integration")
print("   - Integration tests for critical flows")
print("   - E2E tests for user journeys")
print("   - Performance tests")

print("\n" + "=" * 80)
