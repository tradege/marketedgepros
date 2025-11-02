"""
Celery configuration for background tasks
"""
import os
from celery import Celery
from kombu import Exchange, Queue

# Celery configuration
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

# Create Celery app
celery_app = Celery('marketedgepros')

# Configure Celery
celery_app.conf.update(
    broker_url=CELERY_BROKER_URL,
    result_backend=CELERY_RESULT_BACKEND,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    
    # Task routing
    task_routes={
        'src.tasks.email_tasks.*': {'queue': 'emails'},
        'src.tasks.commission_tasks.*': {'queue': 'commissions'},
        'src.tasks.notification_tasks.*': {'queue': 'notifications'},
    },
    
    # Task queues
    task_queues=(
        Queue('default', Exchange('default'), routing_key='default'),
        Queue('emails', Exchange('emails'), routing_key='emails'),
        Queue('commissions', Exchange('commissions'), routing_key='commissions'),
        Queue('notifications', Exchange('notifications'), routing_key='notifications'),
    ),
    
    # Task execution
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_reject_on_worker_lost=True,
    
    # Task time limits
    task_time_limit=300,  # 5 minutes hard limit
    task_soft_time_limit=240,  # 4 minutes soft limit
    
    # Task retry policy
    task_autoretry_for=(Exception,),
    task_retry_kwargs={'max_retries': 3},
    task_retry_backoff=True,
    task_retry_backoff_max=600,
    task_retry_jitter=True,
)

# Auto-discover tasks
celery_app.autodiscover_tasks(['src.tasks'])

