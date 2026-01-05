"""
Flask application initialization
"""
from flask_caching import Cache

# Initialize cache (will be configured in app.py)
cache = Cache()



# Initialize limiter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
limiter = Limiter(key_func=get_remote_address)

