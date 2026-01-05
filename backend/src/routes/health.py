"""
Health Check Endpoint
Monitors system health: database, Redis, Celery, disk space
"""
from flask import Blueprint, jsonify
from src.database import db
from datetime import datetime
import redis
import os
import psutil

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Comprehensive health check endpoint
    Returns system status and component health
    """
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'checks': {}
    }
    
    # Check Database
    try:
        db.session.execute(db.text('SELECT 1'))
        health_status['checks']['database'] = {
            'status': 'healthy',
            'message': 'Database connection OK'
        }
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['database'] = {
            'status': 'unhealthy',
            'message': f'Database error: {str(e)}'
        }
    
    # Check Redis
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        health_status['checks']['redis'] = {
            'status': 'healthy',
            'message': 'Redis connection OK'
        }
    except Exception as e:
        health_status['status'] = 'degraded'
        health_status['checks']['redis'] = {
            'status': 'unhealthy',
            'message': f'Redis error: {str(e)}'
        }
    
    # Check Disk Space
    try:
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        
        if disk_percent > 90:
            health_status['status'] = 'degraded'
            disk_status = 'critical'
        elif disk_percent > 80:
            disk_status = 'warning'
        else:
            disk_status = 'healthy'
        
        health_status['checks']['disk'] = {
            'status': disk_status,
            'used_percent': disk_percent,
            'free_gb': round(disk.free / (1024**3), 2),
            'total_gb': round(disk.total / (1024**3), 2)
        }
    except Exception as e:
        health_status['checks']['disk'] = {
            'status': 'unknown',
            'message': f'Disk check error: {str(e)}'
        }
    
    # Check Memory
    try:
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        if memory_percent > 90:
            health_status['status'] = 'degraded'
            memory_status = 'critical'
        elif memory_percent > 80:
            memory_status = 'warning'
        else:
            memory_status = 'healthy'
        
        health_status['checks']['memory'] = {
            'status': memory_status,
            'used_percent': memory_percent,
            'available_gb': round(memory.available / (1024**3), 2),
            'total_gb': round(memory.total / (1024**3), 2)
        }
    except Exception as e:
        health_status['checks']['memory'] = {
            'status': 'unknown',
            'message': f'Memory check error: {str(e)}'
        }
    
    # Check CPU
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        
        if cpu_percent > 90:
            cpu_status = 'critical'
        elif cpu_percent > 80:
            cpu_status = 'warning'
        else:
            cpu_status = 'healthy'
        
        health_status['checks']['cpu'] = {
            'status': cpu_status,
            'usage_percent': cpu_percent,
            'cores': psutil.cpu_count()
        }
    except Exception as e:
        health_status['checks']['cpu'] = {
            'status': 'unknown',
            'message': f'CPU check error: {str(e)}'
        }
    
    # Determine HTTP status code
    if health_status['status'] == 'healthy':
        status_code = 200
    elif health_status['status'] == 'degraded':
        status_code = 200  # Still operational
    else:
        status_code = 503  # Service unavailable
    
    return jsonify(health_status), status_code


@health_bp.route('/health/live', methods=['GET'])
def liveness():
    """Simple liveness probe - is the app running?"""
    return jsonify({'status': 'alive'}), 200


@health_bp.route('/health/ready', methods=['GET'])
def readiness():
    """Readiness probe - is the app ready to serve traffic?"""
    try:
        # Check database
        db.session.execute(db.text('SELECT 1'))
        return jsonify({'status': 'ready'}), 200
    except Exception as e:
        return jsonify({
            'status': 'not_ready',
            'reason': str(e)
        }), 503
