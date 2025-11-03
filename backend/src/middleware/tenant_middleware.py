"""
Tenant Middleware for Multi-Tenant Support
Automatically detects tenant from subdomain or custom domain
"""
from flask import request, g, abort
from src.models.tenant import Tenant
from functools import wraps
import logging

logger = logging.getLogger(__name__)


def get_tenant_from_request():
    """
    Get tenant from request based on:
    1. Custom domain (e.g., client.com)
    2. Subdomain (e.g., client.marketedgepros.com)
    3. X-Tenant-ID header (for API testing)
    4. tenant_id query parameter (for development)
    
    Returns:
        Tenant: Tenant object or None
    """
    # Check X-Tenant-ID header (for API testing)
    tenant_id_header = request.headers.get('X-Tenant-ID')
    if tenant_id_header:
        try:
            tenant = Tenant.query.get(int(tenant_id_header))
            if tenant and tenant.status == 'active':
                return tenant
        except (ValueError, TypeError):
            pass
    
    # Check tenant_id query parameter (for development)
    tenant_id_param = request.args.get('tenant_id')
    if tenant_id_param:
        try:
            tenant = Tenant.query.get(int(tenant_id_param))
            if tenant and tenant.status == 'active':
                return tenant
        except (ValueError, TypeError):
            pass
    
    # Get host from request
    host = request.host.lower()
    
    # Remove port if present
    if ':' in host:
        host = host.split(':')[0]
    
    # Check for custom domain
    tenant = Tenant.query.filter_by(custom_domain=host, status='active').first()
    if tenant:
        return tenant
    
    # Check for subdomain
    # Expected format: subdomain.marketedgepros.com
    parts = host.split('.')
    
    if len(parts) >= 2:
        # Extract subdomain (first part)
        subdomain = parts[0]
        
        # Skip common subdomains
        if subdomain not in ['www', 'api', 'admin', 'app']:
            tenant = Tenant.query.filter_by(subdomain=subdomain, status='active').first()
            if tenant:
                return tenant
    
    # Default tenant (main platform)
    # You can configure this in settings
    default_tenant = Tenant.query.filter_by(subdomain='main', status='active').first()
    if default_tenant:
        return default_tenant
    
    # If no tenant found, return the first active tenant (fallback)
    return Tenant.query.filter_by(status='active').first()


def tenant_context():
    """
    Middleware to set tenant context for each request
    Should be registered in Flask app
    """
    import os
    from flask import current_app
    
    # Skip in testing mode
    if current_app.config.get('TESTING') or os.environ.get('FLASK_TESTING') == 'true':
        g.tenant = None
        g.tenant_id = None
        return
    
    tenant = get_tenant_from_request()
    
    if tenant:
        g.tenant = tenant
        g.tenant_id = tenant.id
        logger.debug(f"Tenant context set: {tenant.name} (ID: {tenant.id})")
    else:
        g.tenant = None
        g.tenant_id = None
        logger.warning("No tenant found for request")


def require_tenant(f):
    """
    Decorator to require tenant context
    Use on routes that must have a tenant
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, 'tenant') or g.tenant is None:
            logger.error("Tenant required but not found")
            abort(400, description="Tenant not found. Please access via proper domain.")
        return f(*args, **kwargs)
    return decorated_function


def tenant_required(f):
    """
    Decorator to ensure tenant is set in g context
    Alias for require_tenant
    """
    return require_tenant(f)


def get_current_tenant():
    """
    Get current tenant from Flask g context
    
    Returns:
        Tenant: Current tenant or None
    """
    return getattr(g, 'tenant', None)


def get_current_tenant_id():
    """
    Get current tenant ID from Flask g context
    
    Returns:
        int: Current tenant ID or None
    """
    return getattr(g, 'tenant_id', None)


def filter_by_tenant(query, model_class):
    """
    Filter query by current tenant
    
    Args:
        query: SQLAlchemy query object
        model_class: Model class with tenant_id field
        
    Returns:
        Filtered query
    """
    tenant_id = get_current_tenant_id()
    if tenant_id and hasattr(model_class, 'tenant_id'):
        return query.filter_by(tenant_id=tenant_id)
    return query


def ensure_tenant_isolation(data, user=None):
    """
    Ensure data is isolated to current tenant
    Adds tenant_id to data dict if not present
    
    Args:
        data: Dictionary of data
        user: Optional user object (to get tenant_id from)
        
    Returns:
        Updated data dictionary
    """
    if 'tenant_id' not in data:
        # Try to get from current context
        tenant_id = get_current_tenant_id()
        
        # If not in context, try to get from user
        if not tenant_id and user and hasattr(user, 'tenant_id'):
            tenant_id = user.tenant_id
        
        if tenant_id:
            data['tenant_id'] = tenant_id
    
    return data


def init_tenant_middleware(app):
    """
    Initialize tenant middleware for Flask app
    
    Args:
        app: Flask application instance
    """
    import os
    
    # Debug: Check testing flags
    testing_flag = app.config.get('TESTING')
    flask_testing_env = os.environ.get('FLASK_TESTING')
    print(f"DEBUG: TESTING={testing_flag}, FLASK_TESTING={flask_testing_env}")
    
    # Skip tenant middleware in testing mode
    if testing_flag or flask_testing_env == 'true':
        print("DEBUG: Skipping tenant middleware (testing mode)")
        logger.info("Tenant middleware skipped (testing mode)")
        return
    
    @app.before_request
    def set_tenant_context():
        tenant_context()
    
    logger.info("Tenant middleware initialized")

