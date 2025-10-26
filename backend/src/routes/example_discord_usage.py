"""
Example usage of Discord Service in routes
This file shows how to integrate Discord notifications into your existing routes
"""

from services.discord_service import discord_service

# Example 1: New User Registration
# Add this to your registration route
def register_user_example():
    # ... your existing registration code ...
    
    # After successful registration, send Discord notification
    discord_service.notify_new_user_registration(
        user_name=user.full_name,
        user_email=user.email,
        role=user.role
    )


# Example 2: Challenge Passed
# Add this to your challenge completion route
def complete_challenge_example():
    # ... your existing challenge completion code ...
    
    # After trader passes challenge, send Discord notification
    discord_service.notify_challenge_passed(
        trader_name=trader.full_name,
        challenge_name=challenge.name,
        profit=challenge.profit
    )


# Example 3: Withdrawal Request
# Add this to your withdrawal request route
def create_withdrawal_example():
    # ... your existing withdrawal creation code ...
    
    # After withdrawal request created, send Discord notification
    discord_service.notify_withdrawal_request(
        user_name=user.full_name,
        amount=withdrawal.amount,
        method=withdrawal.method
    )


# Example 4: Commission Earned
# Add this to your commission calculation route
def calculate_commission_example():
    # ... your existing commission calculation code ...
    
    # After commission calculated, send Discord notification
    discord_service.notify_commission_earned(
        agent_name=agent.full_name,
        amount=commission.amount,
        trader_name=trader.full_name
    )


# Example 5: KYC Submission
# Add this to your KYC submission route
def submit_kyc_example():
    # ... your existing KYC submission code ...
    
    # After KYC submitted, send Discord notification
    discord_service.notify_kyc_submission(
        user_name=user.full_name,
        user_email=user.email
    )


# Example 6: Payment Received
# Add this to your payment webhook route
def payment_webhook_example():
    # ... your existing payment processing code ...
    
    # After payment confirmed, send Discord notification
    discord_service.notify_payment_received(
        user_name=user.full_name,
        amount=payment.amount,
        program_name=program.name
    )


# Example 7: System Alert
# Add this anywhere you want to send system alerts
def system_alert_example():
    # Send info alert
    discord_service.notify_system_alert(
        alert_type="Database Backup",
        message="Daily database backup completed successfully",
        severity="success"
    )
    
    # Send warning alert
    discord_service.notify_system_alert(
        alert_type="High Server Load",
        message="Server CPU usage is above 80%",
        severity="warning"
    )
    
    # Send error alert
    discord_service.notify_system_alert(
        alert_type="API Error",
        message="Failed to connect to MetaTrader API",
        severity="error"
    )


# Example 8: Custom Notification with Embed
# For more advanced notifications
def custom_notification_example():
    # Create custom embed
    embed = discord_service.create_embed(
        title="🎯 Monthly Target Achieved!",
        description="The platform has reached 1000 active traders!",
        color=0x00FF00,  # Green
        fields=[
            {"name": "Active Traders", "value": "1,000", "inline": True},
            {"name": "Total Volume", "value": "$10M", "inline": True},
            {"name": "Month", "value": "October 2025", "inline": True}
        ],
        footer="MarketEdgePros Analytics"
    )
    
    # Send notification
    discord_service.send_webhook_notification("", embed)

