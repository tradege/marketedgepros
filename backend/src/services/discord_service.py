"""
Discord Service for sending notifications and managing Discord bot
"""
import os
import requests
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class DiscordService:
    """Service for Discord webhook notifications and bot management"""
    
    def __init__(self):
        self.bot_token = os.getenv('DISCORD_BOT_TOKEN')
        self.guild_id = os.getenv('DISCORD_GUILD_ID')
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        self.api_base = 'https://discord.com/api/v10'
    
    def send_webhook_notification(self, message: str, embed: Optional[Dict[str, Any]] = None) -> bool:
        """
        Send notification via Discord webhook
        
        Args:
            message: Text message to send
            embed: Optional Discord embed object
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.webhook_url:
            logger.warning("Discord webhook URL not configured")
            return False
        
        try:
            payload = {"content": message}
            
            if embed:
                payload["embeds"] = [embed]
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            
            response.raise_for_status()
            logger.info(f"Discord notification sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Discord notification: {str(e)}")
            return False
    
    def send_channel_message(self, channel_id: str, message: str, embed: Optional[Dict[str, Any]] = None) -> bool:
        """
        Send message to specific Discord channel using bot
        
        Args:
            channel_id: Discord channel ID
            message: Text message to send
            embed: Optional Discord embed object
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.bot_token:
            logger.warning("Discord bot token not configured")
            return False
        
        try:
            headers = {
                'Authorization': f'Bot {self.bot_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {"content": message}
            
            if embed:
                payload["embeds"] = [embed]
            
            response = requests.post(
                f'{self.api_base}/channels/{channel_id}/messages',
                headers=headers,
                json=payload,
                timeout=10
            )
            
            response.raise_for_status()
            logger.info(f"Message sent to Discord channel {channel_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Discord message: {str(e)}")
            return False
    
    def create_embed(
        self,
        title: str,
        description: str,
        color: int = 0x5865F2,  # Discord blurple
        fields: Optional[list] = None,
        footer: Optional[str] = None,
        thumbnail_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create Discord embed object
        
        Args:
            title: Embed title
            description: Embed description
            color: Embed color (hex as int)
            fields: List of field dicts with 'name' and 'value'
            footer: Footer text
            thumbnail_url: URL for thumbnail image
            
        Returns:
            Dict: Discord embed object
        """
        embed = {
            "title": title,
            "description": description,
            "color": color
        }
        
        if fields:
            embed["fields"] = fields
        
        if footer:
            embed["footer"] = {"text": footer}
        
        if thumbnail_url:
            embed["thumbnail"] = {"url": thumbnail_url}
        
        return embed
    
    # Notification methods for specific events
    
    def notify_new_user_registration(self, user_name: str, user_email: str, role: str) -> bool:
        """Notify about new user registration"""
        embed = self.create_embed(
            title="🎉 New User Registered",
            description=f"A new user has joined MarketEdgePros!",
            color=0x00FF00,  # Green
            fields=[
                {"name": "Name", "value": user_name, "inline": True},
                {"name": "Email", "value": user_email, "inline": True},
                {"name": "Role", "value": role.capitalize(), "inline": True}
            ],
            footer="MarketEdgePros Registration System"
        )
        
        return self.send_webhook_notification("", embed)
    
    def notify_challenge_passed(self, trader_name: str, challenge_name: str, profit: float) -> bool:
        """Notify when a trader passes a challenge"""
        embed = self.create_embed(
            title="🏆 Challenge Passed!",
            description=f"{trader_name} has successfully passed a challenge!",
            color=0xFFD700,  # Gold
            fields=[
                {"name": "Trader", "value": trader_name, "inline": True},
                {"name": "Challenge", "value": challenge_name, "inline": True},
                {"name": "Profit", "value": f"${profit:,.2f}", "inline": True}
            ],
            footer="MarketEdgePros Trading Platform"
        )
        
        return self.send_webhook_notification("", embed)
    
    def notify_withdrawal_request(self, user_name: str, amount: float, method: str) -> bool:
        """Notify about new withdrawal request"""
        embed = self.create_embed(
            title="💰 New Withdrawal Request",
            description=f"A withdrawal request requires approval",
            color=0xFFA500,  # Orange
            fields=[
                {"name": "User", "value": user_name, "inline": True},
                {"name": "Amount", "value": f"${amount:,.2f}", "inline": True},
                {"name": "Method", "value": method, "inline": True}
            ],
            footer="MarketEdgePros Withdrawal System"
        )
        
        return self.send_webhook_notification("", embed)
    
    def notify_commission_earned(self, agent_name: str, amount: float, trader_name: str) -> bool:
        """Notify when an agent earns a commission"""
        embed = self.create_embed(
            title="💵 Commission Earned",
            description=f"{agent_name} earned a new commission!",
            color=0x00FF00,  # Green
            fields=[
                {"name": "Agent", "value": agent_name, "inline": True},
                {"name": "Amount", "value": f"${amount:,.2f}", "inline": True},
                {"name": "From Trader", "value": trader_name, "inline": True}
            ],
            footer="MarketEdgePros Commission System"
        )
        
        return self.send_webhook_notification("", embed)
    
    def notify_kyc_submission(self, user_name: str, user_email: str) -> bool:
        """Notify about new KYC submission"""
        embed = self.create_embed(
            title="📋 New KYC Submission",
            description=f"A new KYC submission requires review",
            color=0x0099FF,  # Blue
            fields=[
                {"name": "User", "value": user_name, "inline": True},
                {"name": "Email", "value": user_email, "inline": True}
            ],
            footer="MarketEdgePros KYC System"
        )
        
        return self.send_webhook_notification("", embed)
    
    def notify_payment_received(self, user_name: str, amount: float, program_name: str) -> bool:
        """Notify about payment received"""
        embed = self.create_embed(
            title="💳 Payment Received",
            description=f"A new payment has been received!",
            color=0x00FF00,  # Green
            fields=[
                {"name": "User", "value": user_name, "inline": True},
                {"name": "Amount", "value": f"${amount:,.2f}", "inline": True},
                {"name": "Program", "value": program_name, "inline": True}
            ],
            footer="MarketEdgePros Payment System"
        )
        
        return self.send_webhook_notification("", embed)
    
    def notify_system_alert(self, alert_type: str, message: str, severity: str = "info") -> bool:
        """Send system alert notification"""
        colors = {
            "info": 0x0099FF,     # Blue
            "warning": 0xFFA500,  # Orange
            "error": 0xFF0000,    # Red
            "success": 0x00FF00   # Green
        }
        
        embed = self.create_embed(
            title=f"🔔 System Alert: {alert_type}",
            description=message,
            color=colors.get(severity, 0x0099FF),
            footer="MarketEdgePros System Monitor"
        )
        
        return self.send_webhook_notification("", embed)


# Create singleton instance
discord_service = DiscordService()

