"""
Production-Grade Caching Service
Using Redis for high-performance caching
"""
from flask_caching import Cache
from functools import wraps
import hashlib
import json

# Initialize cache (will be configured in app factory)
cache = Cache()

def init_cache(app):
    """Initialize cache with app"""
    cache.init_app(app, config={
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_HOST': 'localhost',
        'CACHE_REDIS_PORT': 6379,
        'CACHE_REDIS_DB': 0,
        'CACHE_DEFAULT_TIMEOUT': 300,  # 5 minutes
        'CACHE_KEY_PREFIX': 'marketedge_'
    })
    return cache

def cache_key(*args, **kwargs):
    """Generate cache key from arguments"""
    key_data = {
        'args': args,
        'kwargs': kwargs
    }
    key_string = json.dumps(key_data, sort_keys=True)
    return hashlib.md5(key_string.encode()).hexdigest()

def cached_route(timeout=300):
    """Decorator for caching route responses"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Generate cache key
            key = f'route_{f.__name__}_{cache_key(*args, **kwargs)}'
            
            # Try to get from cache
            cached_response = cache.get(key)
            if cached_response is not None:
                return cached_response
            
            # Execute function
            response = f(*args, **kwargs)
            
            # Cache the response
            cache.set(key, response, timeout=timeout)
            
            return response
        return decorated_function
    return decorator

def invalidate_cache(pattern='*'):
    """Invalidate cache by pattern"""
    try:
        # Get Redis client
        redis_client = cache.cache._write_client
        keys = redis_client.keys(f'marketedge_{pattern}')
        if keys:
            redis_client.delete(*keys)
            return len(keys)
        return 0
    except Exception as e:
        print(f"Error invalidating cache: {e}")
        return 0
