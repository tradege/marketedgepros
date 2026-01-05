"""
Real-Time Monitoring Tasks for PropTradePro
Celery tasks for equity tracking and violation detection
"""

from celery import shared_task
from datetime import datetime, timedelta
from src.database import db
from src.models.trading_program import Challenge
from src.models.mt5_account import MT5Account
from src.services.mt5_service import MT5Service
from src.services.notification_service import NotificationService
import logging

logger = logging.getLogger(__name__)

# Initialize services
mt5_service = MT5Service()
notification_service = NotificationService()


@shared_task(name='monitoring.sync_mt5_trades')
def sync_mt5_trades():
    """
    Sync trades from MT5 for all active challenges
    Runs every 30 seconds
    """
    try:
        # Get all active challenges
        active_challenges = Challenge.query.filter(
            Challenge.status.in_(['active', 'in_progress'])
        ).all()
        
        logger.info(f"Syncing {len(active_challenges)} active challenges")
        
        synced_count = 0
        error_count = 0
        
        for challenge in active_challenges:
            try:
                # Sync individual challenge
                result = sync_challenge_data(challenge.id)
                if result['success']:
                    synced_count += 1
                else:
                    error_count += 1
            except Exception as e:
                logger.error(f"Error syncing challenge {challenge.id}: {str(e)}")
                error_count += 1
        
        logger.info(f"Sync completed: {synced_count} success, {error_count} errors")
        
        return {
            'synced': synced_count,
            'errors': error_count,
            'total': len(active_challenges)
        }
        
    except Exception as e:
        logger.error(f"Error in sync_mt5_trades: {str(e)}")
        return {'error': str(e)}


@shared_task(name='monitoring.sync_challenge_data')
def sync_challenge_data(challenge_id):
    """
    Sync data for a specific challenge
    """
    try:
        challenge = Challenge.query.get(challenge_id)
        if not challenge:
            return {'success': False, 'error': 'Challenge not found'}
        
        if challenge.status not in ['active', 'in_progress']:
            return {'success': False, 'error': 'Challenge not active'}
        
        # Get MT5 account
        mt5_account = MT5Account.query.filter_by(challenge_id=challenge.id).first()
        if not mt5_account:
            return {'success': False, 'error': 'MT5 account not found'}
        
        # Fetch current data from MT5
        mt5_data = mt5_service.get_account_info(mt5_account.mt5_login)
        
        if not mt5_data:
            return {'success': False, 'error': 'Failed to fetch MT5 data'}
        
        # Calculate equity
        balance = float(mt5_data.get('balance', 0))
        equity = float(mt5_data.get('equity', 0))
        open_pnl = equity - balance
        
        # Get commissions and swaps
        commissions = float(mt5_data.get('commission', 0))
        swaps = float(mt5_data.get('swap', 0))
        
        # Update challenge
        challenge.current_balance = balance
        challenge.current_equity = equity
        
        # Update daily drawdown
        day_data = challenge.update_daily_drawdown(
            current_balance=balance,
            current_equity=equity,
            open_pnl=open_pnl,
            commissions=commissions,
            swaps=swaps
        )
        
        # Update total profit/loss
        if challenge.initial_balance:
            total_pnl = equity - float(challenge.initial_balance)
            if total_pnl >= 0:
                challenge.total_profit = total_pnl
                challenge.total_loss = 0
            else:
                challenge.total_profit = 0
                challenge.total_loss = abs(total_pnl)
        
        db.session.commit()
        
        # Log monitoring event
        log_monitoring_event(
            challenge_id=challenge.id,
            event_type='sync',
            event_data={
                'balance': balance,
                'equity': equity,
                'open_pnl': open_pnl,
                'daily_stats': day_data
            }
        )
        
        # Trigger violation check
        check_challenge_violations.delay(challenge.id)
        
        return {
            'success': True,
            'balance': balance,
            'equity': equity,
            'daily_stats': day_data
        }
        
    except Exception as e:
        logger.error(f"Error syncing challenge {challenge_id}: {str(e)}")
        return {'success': False, 'error': str(e)}


@shared_task(name='monitoring.check_all_violations')
def check_all_violations():
    """
    Check all active challenges for violations
    Runs every 10 seconds
    """
    try:
        active_challenges = Challenge.query.filter(
            Challenge.status.in_(['active', 'in_progress'])
        ).all()
        
        logger.info(f"Checking {len(active_challenges)} challenges for violations")
        
        checked_count = 0
        violations_found = 0
        
        for challenge in active_challenges:
            try:
                result = check_challenge_violations(challenge.id)
                checked_count += 1
                
                if result.get('violation_detected'):
                    violations_found += 1
                    
            except Exception as e:
                logger.error(f"Error checking challenge {challenge.id}: {str(e)}")
        
        logger.info(f"Violation check completed: {checked_count} checked, {violations_found} violations")
        
        return {
            'checked': checked_count,
            'violations': violations_found
        }
        
    except Exception as e:
        logger.error(f"Error in check_all_violations: {str(e)}")
        return {'error': str(e)}


@shared_task(name='monitoring.check_challenge_violations')
def check_challenge_violations(challenge_id):
    """
    Check if a specific challenge has violated any rules
    """
    try:
        challenge = Challenge.query.get(challenge_id)
        if not challenge:
            return {'success': False, 'error': 'Challenge not found'}
        
        if challenge.status not in ['active', 'in_progress']:
            return {'success': False, 'error': 'Challenge not active'}
        
        # Get daily stats
        daily_stats = challenge.get_daily_stats()
        
        # Check violations
        violations = []
        
        # Check daily loss
        if challenge.is_daily_loss_exceeded():
            violations.append({
                'type': 'daily_loss',
                'message': 'Daily loss limit exceeded',
                'data': daily_stats
            })
        
        # Check max loss
        if challenge.is_max_loss_exceeded():
            violations.append({
                'type': 'max_loss',
                'message': 'Maximum total loss exceeded',
                'data': daily_stats
            })
        
        # If violations found, take action
        if violations:
            logger.warning(f"Violations detected for challenge {challenge_id}: {violations}")
            
            # Disable account
            disable_result = disable_mt5_account_task.delay(challenge_id, violations)
            
            # Update challenge status
            challenge.status = 'failed'
            challenge.failed_at = datetime.utcnow()
            challenge.failure_reason = violations[0]['message']
            db.session.commit()
            
            # Log violations
            for violation in violations:
                log_violation(
                    challenge_id=challenge.id,
                    violation_type=violation['type'],
                    violation_data=violation['data'],
                    action_taken='account_disabled'
                )
            
            # Send notifications
            send_violation_notifications.delay(challenge_id, violations)
            
            return {
                'success': True,
                'violation_detected': True,
                'violations': violations
            }
        
        # No violations
        return {
            'success': True,
            'violation_detected': False,
            'daily_stats': daily_stats
        }
        
    except Exception as e:
        logger.error(f"Error checking violations for challenge {challenge_id}: {str(e)}")
        return {'success': False, 'error': str(e)}


@shared_task(name='monitoring.disable_mt5_account')
def disable_mt5_account_task(challenge_id, violations):
    """
    Disable MT5 account immediately on violation
    """
    try:
        mt5_account = MT5Account.query.filter_by(challenge_id=challenge_id).first()
        if not mt5_account:
            logger.error(f"MT5 account not found for challenge {challenge_id}")
            return {'success': False, 'error': 'MT5 account not found'}
        
        # Disable trading on MT5
        disable_result = mt5_service.disable_account(mt5_account.mt5_login)
        
        if not disable_result:
            logger.error(f"Failed to disable MT5 account {mt5_account.mt5_login}")
            return {'success': False, 'error': 'Failed to disable MT5 account'}
        
        # Update database
        mt5_account.status = 'disabled'
        mt5_account.disabled_at = datetime.utcnow()
        mt5_account.disable_reason = violations[0]['message']
        db.session.commit()
        
        logger.info(f"MT5 account {mt5_account.mt5_login} disabled for challenge {challenge_id}")
        
        return {
            'success': True,
            'mt5_login': mt5_account.mt5_login,
            'disabled_at': mt5_account.disabled_at.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error disabling MT5 account for challenge {challenge_id}: {str(e)}")
        return {'success': False, 'error': str(e)}


@shared_task(name='monitoring.send_violation_notifications')
def send_violation_notifications(challenge_id, violations):
    """
    Send notifications about violations
    """
    try:
        challenge = Challenge.query.get(challenge_id)
        if not challenge:
            return {'success': False, 'error': 'Challenge not found'}
        
        # Send email to user
        notification_service.send_violation_email(
            user=challenge.user,
            challenge=challenge,
            violations=violations
        )
        
        # Send email to admin
        notification_service.send_admin_alert(
            challenge=challenge,
            violations=violations
        )
        
        # Send Slack/Discord notification
        notification_service.send_slack_alert(
            challenge=challenge,
            violations=violations
        )
        
        logger.info(f"Violation notifications sent for challenge {challenge_id}")
        
        return {'success': True}
        
    except Exception as e:
        logger.error(f"Error sending notifications for challenge {challenge_id}: {str(e)}")
        return {'success': False, 'error': str(e)}


@shared_task(name='monitoring.sync_challenge_immediate')
def sync_challenge_immediate(challenge_id):
    """
    Immediate sync triggered by webhook
    """
    logger.info(f"Immediate sync triggered for challenge {challenge_id}")
    return sync_challenge_data(challenge_id)


# Helper functions

def log_monitoring_event(challenge_id, event_type, event_data):
    """Log monitoring event to database"""
    try:
        from src.models.monitoring import MonitoringEvent
        
        event = MonitoringEvent(
            challenge_id=challenge_id,
            event_type=event_type,
            event_data=event_data
        )
        db.session.add(event)
        db.session.commit()
        
    except Exception as e:
        logger.error(f"Error logging monitoring event: {str(e)}")


def log_violation(challenge_id, violation_type, violation_data, action_taken):
    """Log violation to database"""
    try:
        from src.models.monitoring import ViolationLog
        
        violation = ViolationLog(
            challenge_id=challenge_id,
            violation_type=violation_type,
            violation_data=violation_data,
            action_taken=action_taken
        )
        db.session.add(violation)
        db.session.commit()
        
    except Exception as e:
        logger.error(f"Error logging violation: {str(e)}")


# Celery Beat Schedule Configuration
"""
Add to celeryconfig.py:

CELERYBEAT_SCHEDULE = {
    'sync-mt5-trades': {
        'task': 'monitoring.sync_mt5_trades',
        'schedule': 30.0,  # Every 30 seconds
    },
    'check-violations': {
        'task': 'monitoring.check_all_violations',
        'schedule': 10.0,  # Every 10 seconds
    },
}
"""
