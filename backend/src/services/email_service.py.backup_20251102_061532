"""
Email service using SendGrid
"""
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from flask import current_app, render_template_string
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending transactional emails"""
    
    @staticmethod
    def _get_client():
        """Get SendGrid client"""
        api_key = current_app.config.get('SENDGRID_API_KEY')
        if not api_key:
            logger.warning('SendGrid API key not configured')
            return None
        return SendGridAPIClient(api_key)
    
    @staticmethod
    def _send_email(to_email, subject, html_content, from_email=None):
        """Send email via SendGrid"""
        client = EmailService._get_client()
        if not client:
            logger.error('Cannot send email: SendGrid not configured')
            return False
        
        if not from_email:
            from_email = current_app.config.get('SENDGRID_FROM_EMAIL', 'info@marketedgepros.com')
        
        try:
            message = Mail(
                from_email=Email(from_email),
                to_emails=To(to_email),
                subject=subject,
                html_content=Content("text/html", html_content)
            )
            
            response = client.send(message)
            logger.info(f'Email sent to {to_email}: {response.status_code}')
            return True
            
        except Exception as e:
            logger.error(f'Failed to send email to {to_email}: {str(e)}')
            return False
    
    @staticmethod
    def send_verification_email(user, code_or_token):
        """Send email verification with code or token"""
        # Check if it's a 6-digit code or a token
        is_code = len(code_or_token) == 6 and code_or_token.isdigit()
        
        if is_code:
            # Code-based verification
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .code-box {{ background: white; border: 2px dashed #667eea; padding: 30px; text-align: center; border-radius: 10px; margin: 25px 0; }}
                    .code {{ font-size: 36px; font-weight: bold; letter-spacing: 8px; color: #667eea; font-family: monospace; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Welcome to MarketEdgePros! 🎉</h1>
                    </div>
                    <div class="content">
                        <h2>Hi {user.first_name},</h2>
                        <p>Thank you for registering with MarketEdgePros! We're excited to have you on board.</p>
                        <p>To complete your registration and verify your email address, please enter this verification code:</p>
                        <div class="code-box">
                            <div class="code">{code_or_token}</div>
                        </div>
                        <p style="color: #666; font-size: 14px;">This code will expire in 24 hours.</p>
                        <p>If you didn't create an account with MarketEdgePros, please ignore this email.</p>
                        <p>Best regards,<br>The MarketEdgePros Team</p>
                    </div>
                    <div class="footer">
                        <p>© 2025 MarketEdgePros. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
        else:
            # Token-based verification (URL)
            verification_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:3000')}/verify-email/{code_or_token}"
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Welcome to MarketEdgePros! 🎉</h1>
                    </div>
                    <div class="content">
                        <h2>Hi {user.first_name},</h2>
                        <p>Thank you for registering with MarketEdgePros! We're excited to have you on board.</p>
                        <p>To complete your registration and verify your email address, please click the button below:</p>
                        <p style="text-align: center;">
                            <a href="{verification_url}" class="button">Verify Email Address</a>
                        </p>
                        <p>Or copy and paste this link into your browser:</p>
                        <p style="word-break: break-all; color: #667eea;">{verification_url}</p>
                        <p>This link will expire in 24 hours.</p>
                        <p>If you didn't create an account with MarketEdgePros, please ignore this email.</p>
                        <p>Best regards,<br>The MarketEdgePros Team</p>
                    </div>
                    <div class="footer">
                        <p>© 2025 MarketEdgePros. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
        
        return EmailService._send_email(
            to_email=user.email,
            subject='Verify Your Email - MarketEdgePros',
            html_content=html_content
        )
    
    @staticmethod
    def send_password_reset_email(user, code_or_token):
        """Send password reset email with code or token"""
        # Check if it's a 6-digit code or a token
        is_code = len(code_or_token) == 6 and code_or_token.isdigit()
        
        if is_code:
            # Code-based reset
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .code-box {{ background: white; border: 2px dashed #f5576c; padding: 30px; text-align: center; border-radius: 10px; margin: 25px 0; }}
                    .code {{ font-size: 36px; font-weight: bold; letter-spacing: 8px; color: #f5576c; font-family: monospace; }}
                    .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Password Reset Request 🔒</h1>
                    </div>
                    <div class="content">
                        <h2>Hi {user.first_name},</h2>
                        <p>We received a request to reset your password for your MarketEdgePros account.</p>
                        <p>Enter this code to reset your password:</p>
                        <div class="code-box">
                            <div class="code">{code_or_token}</div>
                        </div>
                        <div class="warning">
                            <strong>⚠️ Security Notice:</strong> This code will expire in 15 minutes for your security.
                        </div>
                        <p>If you didn't request a password reset, please ignore this email and your password will remain unchanged.</p>
                        <p>Best regards,<br>The MarketEdgePros Team</p>
                    </div>
                    <div class="footer">
                        <p>© 2025 MarketEdgePros. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
        else:
            # Token-based reset (URL)
            reset_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:3000')}/reset-password/{code_or_token}"
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .button {{ display: inline-block; padding: 12px 30px; background: #f5576c; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                    .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Password Reset Request 🔒</h1>
                    </div>
                    <div class="content">
                        <h2>Hi {user.first_name},</h2>
                        <p>We received a request to reset your password for your MarketEdgePros account.</p>
                        <p>Click the button below to reset your password:</p>
                        <p style="text-align: center;">
                            <a href="{reset_url}" class="button">Reset Password</a>
                        </p>
                        <p>Or copy and paste this link into your browser:</p>
                        <p style="word-break: break-all; color: #f5576c;">{reset_url}</p>
                        <div class="warning">
                            <strong>⚠️ Security Notice:</strong> This link will expire in 15 minutes for your security.
                        </div>
                        <p>If you didn't request a password reset, please ignore this email and your password will remain unchanged.</p>
                        <p>Best regards,<br>The MarketEdgePros Team</p>
                    </div>
                    <div class="footer">
                        <p>© 2025 MarketEdgePros. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
        
        return EmailService._send_email(
            to_email=user.email,
            subject='Reset Your Password - MarketEdgePros',
            html_content=html_content
        )
    
    @staticmethod
    def send_welcome_email(user):
        """Send welcome email after verification"""
        dashboard_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:3000')}/dashboard"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .features {{ background: white; padding: 20px; border-radius: 5px; margin: 20px 0; }}
                .feature {{ margin: 15px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to MarketEdgePros! 🚀</h1>
                </div>
                <div class="content">
                    <h2>Hi {user.first_name},</h2>
                    <p>Your email has been verified successfully! You're now ready to start your trading journey with MarketEdgePros.</p>
                    
                    <div class="features">
                        <h3>What's Next?</h3>
                        <div class="feature">✅ Browse our trading programs</div>
                        <div class="feature">✅ Choose a challenge that fits your goals</div>
                        <div class="feature">✅ Complete KYC verification</div>
                        <div class="feature">✅ Start trading and earn!</div>
                    </div>
                    
                    <p style="text-align: center;">
                        <a href="{dashboard_url}" class="button">Go to Dashboard</a>
                    </p>
                    
                    <p>If you have any questions, our support team is here to help!</p>
                    <p>Best regards,<br>The MarketEdgePros Team</p>
                </div>
                <div class="footer">
                    <p>© 2025 MarketEdgePros. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return EmailService._send_email(
            to_email=user.email,
            subject='Welcome to MarketEdgePros! 🚀',
            html_content=html_content
        )
    
    @staticmethod
    def send_challenge_purchased_email(user, challenge, program):
        """Send email when challenge is purchased"""
        dashboard_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:3000')}/dashboard"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #11998e; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .info-box {{ background: white; padding: 20px; border-radius: 5px; margin: 20px 0; }}
                .info-row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eee; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Challenge Purchased! 💰</h1>
                </div>
                <div class="content">
                    <h2>Hi {user.first_name},</h2>
                    <p>Congratulations! Your challenge has been purchased successfully.</p>
                    
                    <div class="info-box">
                        <h3>Challenge Details:</h3>
                        <div class="info-row">
                            <span><strong>Program:</strong></span>
                            <span>{program.name}</span>
                        </div>
                        <div class="info-row">
                            <span><strong>Account Size:</strong></span>
                            <span>${program.account_size:,.2f}</span>
                        </div>
                        <div class="info-row">
                            <span><strong>Profit Target:</strong></span>
                            <span>{program.profit_target}%</span>
                        </div>
                        <div class="info-row">
                            <span><strong>Status:</strong></span>
                            <span>{challenge.status.upper()}</span>
                        </div>
                    </div>
                    
                    <p>Your trading account will be set up within 24 hours. You'll receive another email with your login credentials.</p>
                    
                    <p style="text-align: center;">
                        <a href="{dashboard_url}" class="button">View Challenge</a>
                    </p>
                    
                    <p>Good luck with your trading!</p>
                    <p>Best regards,<br>The MarketEdgePros Team</p>
                </div>
                <div class="footer">
                    <p>© 2025 MarketEdgePros. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return EmailService._send_email(
            to_email=user.email,
            subject=f'Challenge Purchased - {program.name}',
            html_content=html_content
        )



    @staticmethod
    def send_commission_earned_email(user, commission_amount, source_user):
        """Send email when user earns a commission"""
        dashboard_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:3000')}/dashboard"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .amount-box {{ background: white; border: 2px solid #f5576c; padding: 30px; text-align: center; border-radius: 10px; margin: 25px 0; }}
                .amount {{ font-size: 48px; font-weight: bold; color: #f5576c; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #f5576c; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>💰 You Earned a Commission!</h1>
                </div>
                <div class="content">
                    <h2>Hi {user.first_name},</h2>
                    <p>Great news! You've earned a commission from your downline.</p>
                    <div class="amount-box">
                        <div class="amount">${commission_amount:.2f}</div>
                        <p style="color: #666; margin-top: 10px;">Commission Earned</p>
                    </div>
                    <p><strong>From:</strong> {source_user.first_name} {source_user.last_name}</p>
                    <p>This commission has been added to your wallet and is available for withdrawal.</p>
                    <p style="text-align: center;">
                        <a href="{dashboard_url}" class="button">View Dashboard</a>
                    </p>
                    <p>Keep up the great work!</p>
                    <p>Best regards,<br>The MarketEdgePros Team</p>
                </div>
                <div class="footer">
                    <p>© 2025 MarketEdgePros. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return EmailService._send_email(
            to_email=user.email,
            subject=f'💰 Commission Earned: ${commission_amount:.2f}',
            html_content=html_content
        )
    
    @staticmethod
    def send_withdrawal_approved_email(user, withdrawal_amount):
        """Send email when withdrawal is approved"""
        dashboard_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:3000')}/dashboard"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .amount-box {{ background: white; border: 2px solid #11998e; padding: 30px; text-align: center; border-radius: 10px; margin: 25px 0; }}
                .amount {{ font-size: 48px; font-weight: bold; color: #11998e; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #11998e; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✅ Withdrawal Approved!</h1>
                </div>
                <div class="content">
                    <h2>Hi {user.first_name},</h2>
                    <p>Good news! Your withdrawal request has been approved.</p>
                    <div class="amount-box">
                        <div class="amount">${withdrawal_amount:.2f}</div>
                        <p style="color: #666; margin-top: 10px;">Withdrawal Amount</p>
                    </div>
                    <p>The funds will be transferred to your account within 3-5 business days.</p>
                    <p style="text-align: center;">
                        <a href="{dashboard_url}" class="button">View Dashboard</a>
                    </p>
                    <p>Thank you for being a valued member of MarketEdgePros!</p>
                    <p>Best regards,<br>The MarketEdgePros Team</p>
                </div>
                <div class="footer">
                    <p>© 2025 MarketEdgePros. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return EmailService._send_email(
            to_email=user.email,
            subject='✅ Withdrawal Approved',
            html_content=html_content
        )
    
    @staticmethod
    def send_withdrawal_rejected_email(user, withdrawal_amount, reason):
        """Send email when withdrawal is rejected"""
        dashboard_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:3000')}/dashboard"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #f5576c; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>❌ Withdrawal Request Rejected</h1>
                </div>
                <div class="content">
                    <h2>Hi {user.first_name},</h2>
                    <p>We're sorry, but your withdrawal request for <strong>${withdrawal_amount:.2f}</strong> has been rejected.</p>
                    <div class="warning">
                        <strong>Reason:</strong> {reason}
                    </div>
                    <p>The funds have been returned to your wallet. If you have any questions or need assistance, please contact our support team.</p>
                    <p style="text-align: center;">
                        <a href="{dashboard_url}" class="button">View Dashboard</a>
                    </p>
                    <p>Best regards,<br>The MarketEdgePros Team</p>
                </div>
                <div class="footer">
                    <p>© 2025 MarketEdgePros. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return EmailService._send_email(
            to_email=user.email,
            subject='❌ Withdrawal Request Rejected',
            html_content=html_content
        )
    
    @staticmethod
    def send_kyc_approved_email(user):
        """Send email when KYC is approved"""
        dashboard_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:3000')}/dashboard"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .success-box {{ background: white; border: 2px solid #11998e; padding: 30px; text-align: center; border-radius: 10px; margin: 25px 0; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #11998e; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✅ KYC Verification Approved!</h1>
                </div>
                <div class="content">
                    <h2>Hi {user.first_name},</h2>
                    <p>Congratulations! Your KYC verification has been approved.</p>
                    <div class="success-box">
                        <h3 style="color: #11998e; margin: 0;">🎉 You're All Set!</h3>
                        <p style="color: #666; margin-top: 10px;">Your account is now fully verified</p>
                    </div>
                    <p>You can now:</p>
                    <ul>
                        <li>Purchase trading challenges</li>
                        <li>Request withdrawals</li>
                        <li>Access all platform features</li>
                    </ul>
                    <p style="text-align: center;">
                        <a href="{dashboard_url}" class="button">Start Trading</a>
                    </p>
                    <p>Thank you for completing the verification process!</p>
                    <p>Best regards,<br>The MarketEdgePros Team</p>
                </div>
                <div class="footer">
                    <p>© 2025 MarketEdgePros. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return EmailService._send_email(
            to_email=user.email,
            subject='✅ KYC Verification Approved',
            html_content=html_content
        )
    
    @staticmethod
    def send_kyc_rejected_email(user, reason):
        """Send email when KYC is rejected"""
        dashboard_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:3000')}/dashboard"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #f5576c; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>❌ KYC Verification Not Approved</h1>
                </div>
                <div class="content">
                    <h2>Hi {user.first_name},</h2>
                    <p>Unfortunately, we were unable to approve your KYC verification at this time.</p>
                    <div class="warning">
                        <strong>Reason:</strong> {reason}
                    </div>
                    <p>Please review the reason above and resubmit your documents. If you need assistance, our support team is here to help.</p>
                    <p style="text-align: center;">
                        <a href="{dashboard_url}" class="button">Resubmit Documents</a>
                    </p>
                    <p>Best regards,<br>The MarketEdgePros Team</p>
                </div>
                <div class="footer">
                    <p>© 2025 MarketEdgePros. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return EmailService._send_email(
            to_email=user.email,
            subject='❌ KYC Verification Not Approved',
            html_content=html_content
        )
    
    @staticmethod
    def send_new_downline_email(user, new_downline):
        """Send email when a new downline joins"""
        dashboard_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:3000')}/dashboard"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .info-box {{ background: white; border: 2px solid #667eea; padding: 20px; border-radius: 10px; margin: 25px 0; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 New Team Member!</h1>
                </div>
                <div class="content">
                    <h2>Hi {user.first_name},</h2>
                    <p>Great news! A new member has joined your team.</p>
                    <div class="info-box">
                        <p><strong>Name:</strong> {new_downline.first_name} {new_downline.last_name}</p>
                        <p><strong>Email:</strong> {new_downline.email}</p>
                        <p><strong>Joined:</strong> Today</p>
                    </div>
                    <p>You'll earn commissions from their activity. Keep growing your team!</p>
                    <p style="text-align: center;">
                        <a href="{dashboard_url}" class="button">View Your Team</a>
                    </p>
                    <p>Best regards,<br>The MarketEdgePros Team</p>
                </div>
                <div class="footer">
                    <p>© 2025 MarketEdgePros. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return EmailService._send_email(
            to_email=user.email,
            subject='🎉 New Team Member Joined!',
            html_content=html_content
        )



    
    # ==================== NOTIFICATION EMAILS ====================
    
    @staticmethod
    def send_notification_email(notification):
        """
        Send email for a notification
        
        Args:
            notification: Notification object
        """
        from src.models.user import User
        
        # Get user
        user = User.query.get(notification.user_id)
        if not user or not user.email:
            return False
        
        # Generate email content
        subject = f"[MarketEdgePros] {notification.title}"
        html_content = EmailService._generate_notification_html(notification, user)
        
        return EmailService._send_email(
            to_email=user.email,
            subject=subject,
            html_content=html_content
        )
    
    @staticmethod
    def _generate_notification_html(notification, user):
        """Generate HTML email body for notification"""
        # Priority color
        priority_colors = {
            'low': '#6B7280',
            'normal': '#3B82F6',
            'high': '#F59E0B',
            'urgent': '#EF4444'
        }
        priority_color = priority_colors.get(notification.priority, '#3B82F6')
        
        # Action button (if applicable)
        action_button = ''
        if notification.type == 'withdrawal':
            action_button = f'<a href="https://marketedgepros.com/trader/withdrawals" style="display: inline-block; padding: 12px 24px; background-color: {priority_color}; color: white; text-decoration: none; border-radius: 6px; margin-top: 20px;">View Withdrawals</a>'
        elif notification.type == 'commission':
            action_button = f'<a href="https://marketedgepros.com/agent/commissions" style="display: inline-block; padding: 12px 24px; background-color: {priority_color}; color: white; text-decoration: none; border-radius: 6px; margin-top: 20px;">View Commissions</a>'
        elif notification.type == 'kyc':
            action_button = f'<a href="https://marketedgepros.com/kyc" style="display: inline-block; padding: 12px 24px; background-color: {priority_color}; color: white; text-decoration: none; border-radius: 6px; margin-top: 20px;">View KYC Status</a>'
        
        user_name = user.first_name or user.name or 'User'
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #F3F4F6;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #F3F4F6; padding: 20px;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                            <h1 style="margin: 0; color: white; font-size: 24px;">MarketEdgePros</h1>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <p style="margin: 0 0 10px 0; color: #6B7280; font-size: 14px;">Hi {user_name},</p>
                            
                            <h2 style="margin: 20px 0; color: #111827; font-size: 20px;">{notification.title}</h2>
                            
                            <div style="background-color: #F9FAFB; border-left: 4px solid {priority_color}; padding: 15px; margin: 20px 0; border-radius: 4px;">
                                <p style="margin: 0; color: #374151; font-size: 16px; line-height: 1.6;">{notification.message}</p>
                            </div>
                            
                            {action_button}
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #F9FAFB; padding: 20px 30px; text-align: center; border-top: 1px solid #E5E7EB;">
                            <p style="margin: 0 0 10px 0; color: #6B7280; font-size: 12px;">
                                This is an automated notification from MarketEdgePros.
                            </p>
                            <p style="margin: 0; color: #6B7280; font-size: 12px;">
                                <a href="https://marketedgepros.com/settings" style="color: #3B82F6; text-decoration: none;">Manage notification preferences</a>
                            </p>
                            <p style="margin: 10px 0 0 0; color: #9CA3AF; font-size: 11px;">
                                © 2025 MarketEdgePros. All rights reserved.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
        """.strip()
    
    @staticmethod
    def queue_email(user_id, to_email, subject, html_body):
        """
        Queue email for async sending (using EmailQueue model)
        
        Args:
            user_id: User ID
            to_email: Recipient email address
            subject: Email subject
            html_body: HTML body
        
        Returns:
            EmailQueue object
        """
        from src.models.notification import EmailQueue
        from src.database import db
        
        email = EmailQueue(
            user_id=user_id,
            to_email=to_email,
            subject=subject,
            body='',  # We use html_body primarily
            html_body=html_body
        )
        
        db.session.add(email)
        db.session.commit()
        
        return email
    
    @staticmethod
    def process_email_queue(batch_size=10):
        """
        Process pending emails in queue
        
        Args:
            batch_size: Number of emails to process in this batch
        
        Returns:
            dict: Statistics about processed emails
        """
        from src.models.notification import EmailQueue
        
        # Get pending emails
        pending_emails = EmailQueue.query.filter_by(status='pending').limit(batch_size).all()
        
        stats = {
            'processed': 0,
            'sent': 0,
            'failed': 0
        }
        
        for email in pending_emails:
            stats['processed'] += 1
            
            # Skip if max attempts reached
            if email.attempts >= email.max_attempts:
                email.mark_as_failed('Max attempts reached')
                stats['failed'] += 1
                continue
            
            # Try to send
            success = EmailService._send_email(
                to_email=email.to_email,
                subject=email.subject,
                html_content=email.html_body or email.body
            )
            
            if success:
                email.mark_as_sent()
                stats['sent'] += 1
            else:
                email.mark_as_failed('SendGrid error')
                stats['failed'] += 1
        
        return stats




def send_course_welcome_email(to_email, name):
    """Send welcome email with course access"""
    subject = "🎓 Welcome to Your Free Trading Course!"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .button {{ display: inline-block; padding: 15px 30px; background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%); color: white; text-decoration: none; border-radius: 8px; font-weight: bold; margin: 20px 0; }}
            .module {{ background: white; padding: 15px; margin: 10px 0; border-left: 4px solid #3b82f6; border-radius: 5px; }}
            .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎓 Welcome to Your Free Trading Course!</h1>
            </div>
            <div class="content">
                <h2>Hi {name},</h2>
                <p>Congratulations! You now have instant access to our comprehensive trading course.</p>
                
                <p><strong>What's included:</strong></p>
                <div class="module">
                    <strong>Module 1:</strong> Trading Fundamentals (45 min)
                </div>
                <div class="module">
                    <strong>Module 2:</strong> Technical Analysis (60 min)
                </div>
                <div class="module">
                    <strong>Module 3:</strong> Risk Management (50 min)
                </div>
                <div class="module">
                    <strong>Module 4:</strong> Trading Strategies (70 min)
                </div>
                <div class="module">
                    <strong>Module 5:</strong> Prop Trading Success (40 min)
                </div>
                
                <p style="text-align: center;">
                    <a href="https://marketedgepros.com/free-course" class="button">
                        Start Learning Now →
                    </a>
                </p>
                
                <p><strong>Next Steps:</strong></p>
                <ul>
                    <li>Complete all 5 modules at your own pace</li>
                    <li>Download the course materials and resources</li>
                    <li>Join our Discord community for support</li>
                    <li>Get your certificate of completion</li>
                </ul>
                
                <p>Ready to take it to the next level? Check out our <a href="https://marketedgepros.com/programs">funded trading programs</a> and start trading with real capital!</p>
                
                <p>Best regards,<br>The MarketEdgePros Team</p>
            </div>
            <div class="footer">
                <p>© 2025 MarketEdgePros. All rights reserved.</p>
                <p>
                    <a href="https://marketedgepros.com/free-course">Course Access</a> | 
                    <a href="https://discord.gg/jKbmeSe7">Join Discord</a> | 
                    <a href="https://marketedgepros.com/contact">Contact Us</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return EmailService._send_email(to_email, subject, html_content)

