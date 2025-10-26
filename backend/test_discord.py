"""
Test Discord Integration
Run this file to test if Discord notifications are working
"""
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.discord_service import discord_service

def test_system_alert():
    """Test basic system alert"""
    print("🔔 Sending test notification to Discord...")
    
    result = discord_service.notify_system_alert(
        alert_type="Integration Test",
        message="Discord integration is working! 🎉\n\nThis is a test message from MarketEdgePros backend.",
        severity="success"
    )
    
    if result:
        print("✅ SUCCESS! Check your Discord channel for the notification!")
    else:
        print("❌ FAILED! Check your DISCORD_WEBHOOK_URL in .env file")
    
    return result

def test_new_user():
    """Test new user registration notification"""
    print("\n🔔 Sending new user registration notification...")
    
    result = discord_service.notify_new_user_registration(
        user_name="John Doe (Test User)",
        user_email="test@marketedgepros.com",
        role="trader"
    )
    
    if result:
        print("✅ SUCCESS! New user notification sent!")
    else:
        print("❌ FAILED!")
    
    return result

def test_challenge_passed():
    """Test challenge passed notification"""
    print("\n🔔 Sending challenge passed notification...")
    
    result = discord_service.notify_challenge_passed(
        trader_name="Jane Smith (Test Trader)",
        challenge_name="Phase 1 - $50K Challenge",
        profit=5250.00
    )
    
    if result:
        print("✅ SUCCESS! Challenge notification sent!")
    else:
        print("❌ FAILED!")
    
    return result

def test_custom_embed():
    """Test custom embed notification"""
    print("\n🔔 Sending custom embed notification...")
    
    embed = discord_service.create_embed(
        title="🎯 Test: Custom Notification",
        description="This is a custom notification with multiple fields!",
        color=0x5865F2,  # Discord blurple
        fields=[
            {"name": "Field 1", "value": "Value 1", "inline": True},
            {"name": "Field 2", "value": "Value 2", "inline": True},
            {"name": "Field 3", "value": "Value 3", "inline": True},
            {"name": "Long Field", "value": "This is a longer field that spans the full width", "inline": False}
        ],
        footer="MarketEdgePros Test Suite"
    )
    
    result = discord_service.send_webhook_notification("", embed)
    
    if result:
        print("✅ SUCCESS! Custom embed sent!")
    else:
        print("❌ FAILED!")
    
    return result

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Discord Integration Test Suite")
    print("=" * 60)
    
    # Test 1: System Alert
    test1 = test_system_alert()
    
    # Test 2: New User
    test2 = test_new_user()
    
    # Test 3: Challenge Passed
    test3 = test_challenge_passed()
    
    # Test 4: Custom Embed
    test4 = test_custom_embed()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print("=" * 60)
    print(f"System Alert:     {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"New User:         {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"Challenge Passed: {'✅ PASS' if test3 else '❌ FAIL'}")
    print(f"Custom Embed:     {'✅ PASS' if test4 else '❌ FAIL'}")
    print("=" * 60)
    
    if all([test1, test2, test3, test4]):
        print("\n🎉 All tests passed! Discord integration is working perfectly!")
    else:
        print("\n⚠️  Some tests failed. Check your .env configuration:")
        print("   - DISCORD_WEBHOOK_URL should be set")
        print("   - Webhook should not be deleted in Discord")
        print("   - Check backend logs for errors")

if __name__ == "__main__":
    main()

