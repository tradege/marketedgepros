#!/usr/bin/env python3
"""
Celery worker for processing email queue
"""
from celery import Celery
from celery.schedules import crontab
import os
from src.app import create_app
from src.models.notification import EmailQueue
from src.database import db
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime

# Initialize Flask app
flask_app = create_app()

# Initialize Celery
celery = Celery(
    'marketedgepros',
    broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    backend=os.getenv('REDIS_URL', 'redis://localhost:6379/0')
)

# Celery configuration
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    beat_schedule={
        'process-email-queue': {
            'task': 'celery_worker.process_email_queue',
            'schedule': 10.0,  # Run every 10 seconds
        },
    }
)

@celery.task(name='celery_worker.process_email_queue')
def process_email_queue():
    """Process pending emails in the queue"""
    with flask_app.app_context():
        try:
            # Get pending emails
            pending_emails = EmailQueue.query.filter_by(status='pending').limit(10).all()
            
            if not pending_emails:
                print('No pending emails')
                return {'processed': 0}
            
            processed = 0
            failed = 0
            
            for email in pending_emails:
                try:
                    print(f'Sending email to: {email.to_email}')
                    
                    # Create SendGrid message
                    message = Mail(
                        from_email=os.getenv('SENDGRID_FROM_EMAIL', 'noreply@marketedgepros.com'),
                        to_emails=email.to_email,
                        subject=email.subject,
                        html_content=email.html_body
                    )
                    
                    # Send via SendGrid
                    sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
                    response = sg.send(message)
                    
                    # Update status
                    email.status = 'sent'
                    email.sent_at = datetime.utcnow()
                    db.session.commit()
                    
                    processed += 1
                    print(f'✅ Email sent! Status: {response.status_code}')
                    
                except Exception as e:
                    print(f'❌ Failed to send email: {e}')
                    email.status = 'failed'
                    email.error_message = str(e)
                    db.session.commit()
                    failed += 1
            
            return {
                'processed': processed,
                'failed': failed,
                'total': len(pending_emails)
            }
            
        except Exception as e:
            print(f'❌ Error processing email queue: {e}')
            return {'error': str(e)}

if __name__ == '__main__':
    celery.start()
