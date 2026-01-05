"""
Enhanced Logging Configuration for MarketEdgePros
Provides structured JSON logging with context and performance tracking
"""
import logging
import logging.handlers
import json
import os
from datetime import datetime
from flask import request, g, has_request_context
from functools import wraps
import time

class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging
    Outputs logs in JSON format for easy parsing and analysis
    """
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add request context if available
        if has_request_context():
            log_data['request'] = {
                'method': request.method,
                'path': request.path,
                'ip': request.remote_addr,
                'user_agent': request.user_agent.string if request.user_agent else None
            }
            
            # Add user info if authenticated
            if hasattr(g, 'current_user') and g.current_user:
                log_data['user'] = {
                    'id': g.current_user.id,
                    'email': g.current_user.email,
                    'role': g.current_user.role
                }
        
        # Add extra fields from record
        if hasattr(record, 'extra_data'):
            log_data['extra'] = record.extra_data
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': self.formatException(record.exc_info)
            }
        
        return json.dumps(log_data)


class ContextFilter(logging.Filter):
    """
    Add contextual information to log records
    """
    
    def filter(self, record):
        # Add request ID if available
        if has_request_context() and hasattr(g, 'request_id'):
            record.request_id = g.request_id
        else:
            record.request_id = None
        
        return True


def setup_logging(app):
    """
    Setup comprehensive logging for the application
    
    Args:
        app: Flask application instance
    """
    
    # Get log level from config
    log_level = app.config.get('LOG_LEVEL', 'INFO')
    log_dir = app.config.get('LOG_DIR', '/var/log/marketedgepros')
    
    # Create log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    
    # Remove default handlers
    app.logger.handlers = []
    
    # Set log level
    app.logger.setLevel(getattr(logging, log_level))
    
    # ===== Console Handler (for development) =====
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if app.debug else logging.INFO)
    
    if app.debug:
        # Human-readable format for development
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    else:
        # JSON format for production
        console_formatter = JSONFormatter()
    
    console_handler.setFormatter(console_formatter)
    console_handler.addFilter(ContextFilter())
    app.logger.addHandler(console_handler)
    
    # ===== File Handler (rotating) =====
    file_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(log_dir, 'app.log'),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(JSONFormatter())
    file_handler.addFilter(ContextFilter())
    app.logger.addHandler(file_handler)
    
    # ===== Error File Handler (errors only) =====
    error_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(log_dir, 'error.log'),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(JSONFormatter())
    error_handler.addFilter(ContextFilter())
    app.logger.addHandler(error_handler)
    
    # ===== Security Log Handler (auth, access control) =====
    security_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(log_dir, 'security.log'),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=20  # Keep more security logs
    )
    security_handler.setLevel(logging.INFO)
    security_handler.setFormatter(JSONFormatter())
    security_handler.addFilter(ContextFilter())
    
    # Create security logger
    security_logger = logging.getLogger('security')
    security_logger.setLevel(logging.INFO)
    security_logger.addHandler(security_handler)
    security_logger.propagate = False
    
    app.logger.info('Logging system initialized', extra={
        'extra_data': {
            'log_level': log_level,
            'log_dir': log_dir
        }
    })


def log_request_start():
    """
    Log request start and set up request context
    Call this at the beginning of each request
    """
    import uuid
    
    # Generate unique request ID
    g.request_id = str(uuid.uuid4())
    g.request_start_time = time.time()
    
    # Log request start
    logging.getLogger('app').info('Request started', extra={
        'extra_data': {
            'request_id': g.request_id,
            'method': request.method,
            'path': request.path,
            'query_string': request.query_string.decode('utf-8'),
            'ip': request.remote_addr,
            'user_agent': request.user_agent.string if request.user_agent else None
        }
    })


def log_request_end(response):
    """
    Log request completion with duration and status
    Call this at the end of each request
    
    Args:
        response: Flask response object
    
    Returns:
        response: Unmodified response object
    """
    if hasattr(g, 'request_start_time'):
        duration = time.time() - g.request_start_time
        
        logging.getLogger('app').info('Request completed', extra={
            'extra_data': {
                'request_id': g.request_id if hasattr(g, 'request_id') else None,
                'status_code': response.status_code,
                'duration_ms': round(duration * 1000, 2),
                'response_size': len(response.get_data())
            }
        })
    
    return response


def log_security_event(event_type, user_id=None, details=None):
    """
    Log security-related events
    
    Args:
        event_type: Type of security event (login, logout, failed_login, etc.)
        user_id: ID of the user involved
        details: Additional details about the event
    """
    security_logger = logging.getLogger('security')
    
    event_data = {
        'event_type': event_type,
        'user_id': user_id,
        'ip': request.remote_addr if has_request_context() else None,
        'user_agent': request.user_agent.string if has_request_context() and request.user_agent else None
    }
    
    if details:
        event_data.update(details)
    
    security_logger.info(f'Security event: {event_type}', extra={
        'extra_data': event_data
    })


def log_performance(operation, duration_ms, details=None):
    """
    Log performance metrics
    
    Args:
        operation: Name of the operation
        duration_ms: Duration in milliseconds
        details: Additional details
    """
    logger = logging.getLogger('performance')
    
    perf_data = {
        'operation': operation,
        'duration_ms': duration_ms
    }
    
    if details:
        perf_data.update(details)
    
    # Warn if operation is slow
    level = logging.WARNING if duration_ms > 1000 else logging.INFO
    
    logger.log(level, f'Performance: {operation}', extra={
        'extra_data': perf_data
    })


def log_database_query(query, duration_ms, params=None):
    """
    Log database queries for performance monitoring
    
    Args:
        query: SQL query string
        duration_ms: Query duration in milliseconds
        params: Query parameters
    """
    logger = logging.getLogger('database')
    
    query_data = {
        'query': query[:500],  # Truncate long queries
        'duration_ms': duration_ms,
        'params': params
    }
    
    # Warn if query is slow
    level = logging.WARNING if duration_ms > 500 else logging.DEBUG
    
    logger.log(level, 'Database query', extra={
        'extra_data': query_data
    })


def performance_monitor(operation_name=None):
    """
    Decorator to monitor function performance
    
    Usage:
        @performance_monitor('user_registration')
        def register_user():
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000
                
                log_performance(
                    operation=operation_name or func.__name__,
                    duration_ms=round(duration_ms, 2),
                    details={'status': 'success'}
                )
                
                return result
            
            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000
                
                log_performance(
                    operation=operation_name or func.__name__,
                    duration_ms=round(duration_ms, 2),
                    details={
                        'status': 'error',
                        'error': str(e)
                    }
                )
                
                raise
        
        return wrapper
    return decorator


# Example usage in routes:
"""
from src.logging_config import log_security_event, performance_monitor

@auth_bp.route('/login', methods=['POST'])
@performance_monitor('user_login')
def login():
    # ... login logic ...
    
    if success:
        log_security_event('login_success', user_id=user.id)
    else:
        log_security_event('login_failed', details={'email': email})
    
    return response
"""

