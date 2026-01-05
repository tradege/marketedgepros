"""
Advanced Logging with Email Alerts
"""
import logging
import logging.handlers
import os
from flask import current_app
from src.services.email_service import EmailService


class EmailAlertHandler(logging.Handler):
    """Custom logging handler that sends email alerts for critical errors"""
    
    def __init__(self, email_to, email_from, subject):
        super().__init__()
        self.email_to = email_to
        self.email_from = email_from
        self.subject = subject
        self.setLevel(logging.ERROR)  # Only send emails for ERROR and CRITICAL
    
    def emit(self, record):
        """Send email alert for error"""
        try:
            log_entry = self.format(record)
            
            # Email body
            body = f"""
<h2>Critical Error Alert</h2>
<p><strong>Time:</strong> {record.asctime}</p>
<p><strong>Level:</strong> {record.levelname}</p>
<p><strong>Logger:</strong> {record.name}</p>
<p><strong>Message:</strong></p>
<pre>{record.getMessage()}</pre>

<p><strong>Location:</strong></p>
<pre>File: {record.pathname}
Line: {record.lineno}
Function: {record.funcName}</pre>

{f'<p><strong>Exception:</strong></p><pre>{self.format_exception(record.exc_info)}</pre>' if record.exc_info else ''}

<hr>
<p><em>This is an automated alert from MarketEdgePros monitoring system.</em></p>
            """
            
            # Send email
            EmailService.send_email(
                to_email=self.email_to,
                subject=self.subject,
                html_body=body
            )
        except Exception as e:
            # Don't let email sending errors crash the app
            print(f"Failed to send error alert email: {e}")
    
    def format_exception(self, exc_info):
        """Format exception info"""
        if exc_info:
            import traceback
            return ''.join(traceback.format_exception(*exc_info))
        return ''


def setup_advanced_logging(app):
    """Setup advanced logging with file rotation and email alerts"""
    
    # Get config
    log_level = app.config.get('LOG_LEVEL', 'INFO')
    log_file = app.config.get('LOG_FILE', 'logs/app.log')
    max_bytes = app.config.get('LOG_MAX_BYTES', 10485760)  # 10MB
    backup_count = app.config.get('LOG_BACKUP_COUNT', 10)
    
    # Create logs directory if not exists
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    # Setup rotating file handler
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    file_handler.setLevel(getattr(logging, log_level))
    
    # Format
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # Add file handler
    app.logger.addHandler(file_handler)
    app.logger.setLevel(getattr(logging, log_level))
    
    # Setup email alerts for critical errors
    if app.config.get('ALERT_EMAIL_ENABLED'):
        email_handler = EmailAlertHandler(
            email_to=app.config.get('ALERT_EMAIL_TO'),
            email_from=app.config.get('ALERT_EMAIL_FROM'),
            subject=app.config.get('ALERT_EMAIL_SUBJECT', 'Critical Error Alert')
        )
        email_handler.setFormatter(formatter)
        app.logger.addHandler(email_handler)
        app.logger.info('Email alerts enabled for critical errors')
    
    app.logger.info(f'Advanced logging initialized - Level: {log_level}, File: {log_file}')
    
    return app.logger
