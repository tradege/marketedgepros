"""
Course Drip Campaign - Automated Email Scheduler
Sends course modules to enrolled students over 10 days
"""
from datetime import datetime, timedelta
from ..database import db
from ..models.course_enrollment import CourseEnrollment
from ..services.email_service import EmailService
import logging

logger = logging.getLogger(__name__)


def send_course_module_emails():
    """
    Send course module emails based on enrollment date
    Run this task daily (via cron or scheduler)
    """
    now = datetime.utcnow()
    
    # Get all active enrollments (not unsubscribed)
    enrollments = CourseEnrollment.query.filter_by(unsubscribed=False).all()
    
    for enrollment in enrollments:
        days_since_enrollment = (now - enrollment.enrolled_at).days
        
        # Module 1 - Day 2
        if days_since_enrollment >= 2 and not enrollment.module_1_sent:
            send_module_email(enrollment, 1)
            enrollment.module_1_sent = True
            enrollment.module_1_sent_at = now
            db.session.commit()
            logger.info(f"Sent Module 1 to {enrollment.email}")
        
        # Module 2 - Day 4
        elif days_since_enrollment >= 4 and not enrollment.module_2_sent:
            send_module_email(enrollment, 2)
            enrollment.module_2_sent = True
            enrollment.module_2_sent_at = now
            db.session.commit()
            logger.info(f"Sent Module 2 to {enrollment.email}")
        
        # Module 3 - Day 6
        elif days_since_enrollment >= 6 and not enrollment.module_3_sent:
            send_module_email(enrollment, 3)
            enrollment.module_3_sent = True
            enrollment.module_3_sent_at = now
            db.session.commit()
            logger.info(f"Sent Module 3 to {enrollment.email}")
        
        # Module 4 - Day 8
        elif days_since_enrollment >= 8 and not enrollment.module_4_sent:
            send_module_email(enrollment, 4)
            enrollment.module_4_sent = True
            enrollment.module_4_sent_at = now
            db.session.commit()
            logger.info(f"Sent Module 4 to {enrollment.email}")
        
        # Module 5 - Day 10
        elif days_since_enrollment >= 10 and not enrollment.module_5_sent:
            send_module_email(enrollment, 5)
            enrollment.module_5_sent = True
            enrollment.module_5_sent_at = now
            db.session.commit()
            logger.info(f"Sent Module 5 to {enrollment.email}")


def send_module_email(enrollment, module_number):
    """Send specific module email"""
    modules = {
        1: {
            'title': 'Module 1: Trading Fundamentals',
            'duration': '45 minutes',
            'topics': [
                'Understanding Prop Trading',
                'Market Structure Basics',
                'Order Types & Execution',
                'Platform Navigation'
            ],
            'cta': 'Start Module 1'
        },
        2: {
            'title': 'Module 2: Risk Management Mastery',
            'duration': '60 minutes',
            'topics': [
                'Position Sizing Strategies',
                'Stop Loss Placement',
                'Risk-Reward Ratios',
                'Drawdown Management'
            ],
            'cta': 'Start Module 2'
        },
        3: {
            'title': 'Module 3: Technical Analysis Deep Dive',
            'duration': '75 minutes',
            'topics': [
                'Chart Patterns Recognition',
                'Key Indicators & Oscillators',
                'Support & Resistance Levels',
                'Trend Analysis'
            ],
            'cta': 'Start Module 3'
        },
        4: {
            'title': 'Module 4: Trading Psychology',
            'duration': '50 minutes',
            'topics': [
                'Emotional Control Techniques',
                'Discipline & Consistency',
                'Handling Losses',
                'Building Confidence'
            ],
            'cta': 'Start Module 4'
        },
        5: {
            'title': 'Module 5: Advanced Strategies',
            'duration': '90 minutes',
            'topics': [
                'Scalping Techniques',
                'Swing Trading Setups',
                'News Trading Strategies',
                'Multi-Timeframe Analysis'
            ],
            'cta': 'Start Module 5'
        }
    }
    
    module = modules[module_number]
    topics_html = ''.join([f'<li>{topic}</li>' for topic in module['topics']])
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .module-box {{ background: white; padding: 25px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #667eea; }}
            .topics {{ background: #f0f4ff; padding: 20px; border-radius: 5px; margin: 15px 0; }}
            .topics ul {{ margin: 10px 0; padding-left: 20px; }}
            .topics li {{ margin: 8px 0; }}
            .button {{ display: inline-block; padding: 15px 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; }}
            .progress {{ background: #e0e0e0; height: 8px; border-radius: 10px; margin: 20px 0; }}
            .progress-bar {{ background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); height: 100%; border-radius: 10px; width: {module_number * 20}%; }}
            .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎓 Free Trading Course</h1>
                <p style="margin: 10px 0 0 0; font-size: 18px;">Module {module_number} of 5</p>
            </div>
            <div class="content">
                <h2>Hi {enrollment.name or 'Trader'},</h2>
                <p>Your next module is ready! 🚀</p>
                
                <div class="module-box">
                    <h3 style="color: #667eea; margin-top: 0;">{module['title']}</h3>
                    <p><strong>⏱️ Duration:</strong> {module['duration']}</p>
                    
                    <div class="topics">
                        <strong>📚 What You'll Learn:</strong>
                        <ul>
                            {topics_html}
                        </ul>
                    </div>
                </div>
                
                <p><strong>Your Progress:</strong></p>
                <div class="progress">
                    <div class="progress-bar"></div>
                </div>
                <p style="text-align: center; color: #666;">{module_number} of 5 modules ({module_number * 20}% complete)</p>
                
                <p style="text-align: center;">
                    <a href="https://marketedgepros.com/free-course" class="button">{module['cta']}</a>
                </p>
                
                <p style="margin-top: 30px;">Keep up the great work! You're making excellent progress on your trading journey.</p>
                
                <p>Best regards,<br>The MarketEdgePros Team</p>
                
                <p style="font-size: 12px; color: #999; margin-top: 30px;">
                    Don't want to receive these emails? <a href="https://marketedgepros.com/unsubscribe?email={enrollment.email}" style="color: #667eea;">Unsubscribe here</a>
                </p>
            </div>
            <div class="footer">
                <p>© 2025 MarketEdgePros. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return EmailService._send_email(
        to_email=enrollment.email,
        subject=f"📚 {module['title']} - Free Trading Course",
        html_content=html_content
    )

