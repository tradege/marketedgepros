"""
HTML Email Templates for MarketEdgePros
"""

# Base template with styling
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 600px;
            margin: 20px auto;
            background: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #ffffff;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 28px;
        }
        .content {
            padding: 30px;
        }
        .content h2 {
            color: #667eea;
            margin-top: 0;
        }
        .button {
            display: inline-block;
            padding: 12px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #ffffff;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px 0;
            font-weight: bold;
        }
        .button:hover {
            opacity: 0.9;
        }
        .footer {
            background: #f8f8f8;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #666;
        }
        .highlight {
            background: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin: 15px 0;
        }
        .code {
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
            letter-spacing: 5px;
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 5px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>MarketEdgePros</h1>
        </div>
        <div class="content">
            {{ content }}
        </div>
        <div class="footer">
            <p>&copy; 2025 MarketEdgePros. All rights reserved.</p>
            <p>This email was sent to {{ user_email }}. If you didn't request this, please ignore it.</p>
        </div>
    </div>
</body>
</html>
"""


def get_welcome_template():
    """Welcome email template"""
    content = """
        <h2>Welcome to MarketEdgePros! 🎉</h2>
        <p>Hi {{ user_name }},</p>
        <p>Thank you for joining MarketEdgePros! We're excited to have you on board.</p>
        <p>With MarketEdgePros, you can:</p>
        <ul>
            <li>Take on trading challenges and earn funding</li>
            <li>Build your trading career with professional support</li>
            <li>Earn commissions by referring other traders</li>
        </ul>
        <p>Ready to get started?</p>
        <a href="{{ login_url }}" class="button">Login to Your Account</a>
        <p>If you have any questions, feel free to reach out to our support team.</p>
        <p>Best regards,<br>The MarketEdgePros Team</p>
    """
    return BASE_TEMPLATE.replace('{{ content }}', content)


def get_verification_template():
    """Email verification template"""
    content = """
        <h2>Verify Your Email Address</h2>
        <p>Hi {{ user_name }},</p>
        <p>Thank you for registering with MarketEdgePros! To complete your registration, please verify your email address using the code below:</p>
        <div class="code">{{ verification_code }}</div>
        <p>This code will expire in 24 hours.</p>
        <div class="highlight">
            <strong>Important:</strong> If you didn't create an account with MarketEdgePros, please ignore this email.
        </div>
        <p>Best regards,<br>The MarketEdgePros Team</p>
    """
    return BASE_TEMPLATE.replace('{{ content }}', content)


def get_password_reset_template():
    """Password reset template"""
    content = """
        <h2>Reset Your Password</h2>
        <p>Hi {{ user_name }},</p>
        <p>We received a request to reset your password. Click the button below to create a new password:</p>
        <a href="{{ reset_url }}" class="button">Reset Password</a>
        <p>This link will expire in 1 hour.</p>
        <div class="highlight">
            <strong>Security Tip:</strong> If you didn't request a password reset, please ignore this email and ensure your account is secure.
        </div>
        <p>Best regards,<br>The MarketEdgePros Team</p>
    """
    return BASE_TEMPLATE.replace('{{ content }}', content)


def get_challenge_purchased_template():
    """Challenge purchase confirmation template"""
    content = """
        <h2>Challenge Purchased Successfully! 🎯</h2>
        <p>Hi {{ user_name }},</p>
        <p>Congratulations! Your challenge "<strong>{{ challenge_name }}</strong>" has been purchased successfully.</p>
        <p>You can now start trading and working towards your goals.</p>
        <a href="{{ challenge_url }}" class="button">View Challenge Details</a>
        <p><strong>Next Steps:</strong></p>
        <ul>
            <li>Review your challenge requirements</li>
            <li>Set up your trading account</li>
            <li>Start trading and tracking your progress</li>
        </ul>
        <p>Good luck with your trading journey!</p>
        <p>Best regards,<br>The MarketEdgePros Team</p>
    """
    return BASE_TEMPLATE.replace('{{ content }}', content)


def get_commission_earned_template():
    """Commission earned notification template"""
    content = """
        <h2>You've Earned a Commission! 💰</h2>
        <p>Hi {{ user_name }},</p>
        <p>Great news! You've earned a <strong>{{ commission_type }}</strong> commission.</p>
        <div class="highlight">
            <h3 style="margin: 0;">Commission Amount: ${{ amount }}</h3>
        </div>
        <p>This commission has been added to your account balance.</p>
        <a href="https://marketedgepros.com/admin/commissions" class="button">View Commissions</a>
        <p>Keep up the great work building your network!</p>
        <p>Best regards,<br>The MarketEdgePros Team</p>
    """
    return BASE_TEMPLATE.replace('{{ content }}', content)


def get_withdrawal_approved_template():
    """Withdrawal approved notification template"""
    content = """
        <h2>Withdrawal Approved! ✅</h2>
        <p>Hi {{ user_name }},</p>
        <p>Your withdrawal request has been approved!</p>
        <div class="highlight">
            <h3 style="margin: 0;">Withdrawal Amount: ${{ amount }}</h3>
        </div>
        <p>The funds will be transferred to your designated account within 3-5 business days.</p>
        <a href="https://marketedgepros.com/admin/withdrawals" class="button">View Withdrawal Details</a>
        <p><strong>What's Next:</strong></p>
        <ul>
            <li>You'll receive a confirmation once the transfer is complete</li>
            <li>Check your bank account in 3-5 business days</li>
            <li>Contact support if you have any questions</li>
        </ul>
        <p>Thank you for being part of MarketEdgePros!</p>
        <p>Best regards,<br>The MarketEdgePros Team</p>
    """
    return BASE_TEMPLATE.replace('{{ content }}', content)


def get_challenge_passed_template():
    """Challenge passed notification template"""
    content = """
        <h2>Congratulations! Challenge Passed! 🏆</h2>
        <p>Hi {{ user_name }},</p>
        <p>Excellent work! You've successfully passed your challenge "<strong>{{ challenge_name }}</strong>"!</p>
        <div class="highlight">
            <h3 style="margin: 0;">Achievement Unlocked!</h3>
            <p>You've demonstrated exceptional trading skills.</p>
        </div>
        <a href="{{ challenge_url }}" class="button">View Results</a>
        <p><strong>What's Next:</strong></p>
        <ul>
            <li>Review your trading performance</li>
            <li>Claim your rewards</li>
            <li>Take on the next challenge</li>
        </ul>
        <p>Keep up the excellent work!</p>
        <p>Best regards,<br>The MarketEdgePros Team</p>
    """
    return BASE_TEMPLATE.replace('{{ content }}', content)


def get_challenge_failed_template():
    """Challenge failed notification template"""
    content = """
        <h2>Challenge Update</h2>
        <p>Hi {{ user_name }},</p>
        <p>We wanted to let you know that your challenge "<strong>{{ challenge_name }}</strong>" has ended.</p>
        <p>Don't be discouraged! Every trader faces setbacks, and this is an opportunity to learn and improve.</p>
        <a href="{{ challenge_url }}" class="button">Review Performance</a>
        <p><strong>Next Steps:</strong></p>
        <ul>
            <li>Analyze your trades to identify areas for improvement</li>
            <li>Review your risk management strategy</li>
            <li>Consider retaking the challenge when you're ready</li>
        </ul>
        <p>Remember, success in trading is a journey. We're here to support you!</p>
        <p>Best regards,<br>The MarketEdgePros Team</p>
    """
    return BASE_TEMPLATE.replace('{{ content }}', content)

