"""
Main Flask application factory
"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from src.config import get_config
from src.database import db, init_db
from src.middleware.tenant_middleware import init_tenant_middleware
import logging


def create_app(config_name=None):
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    if config_name:
        from src.config import config
        app.config.from_object(config[config_name])
    else:
        config_class = get_config()
        app.config.from_object(config_class)
    
    # Initialize extensions
    init_db(app)
    
    # Initialize caching
    from src import cache
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})
    
    # Initialize tenant middleware
    init_tenant_middleware(app)
    
    # Enable CORS
    cors_origins = app.config.get('CORS_ORIGINS', '*')
    if isinstance(cors_origins, str):
        cors_origins = cors_origins.split(',')
    elif not isinstance(cors_origins, list):
        cors_origins = ['*']
    CORS(app, 
         resources={r"/api/*": {
             "origins": cors_origins,
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True
         }})
    
    # Rate Limiting
    if app.config.get('RATELIMIT_ENABLED'):
        limiter = Limiter(
            app=app,
            key_func=get_remote_address,
            storage_uri=app.config.get('RATELIMIT_STORAGE_URL'),
            default_limits=["5000 per day", "1000 per hour"]
        )
        app.limiter = limiter
    
    # Security Headers
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://api.marketedgepros.com"
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        return response
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Register blueprints
    from src.routes.auth import auth_bp
    from src.routes.users import users_bp
    from src.routes.profile import profile_bp
    from src.routes.programs import programs_bp
    from src.routes.payments import payments_bp
    from src.routes.uploads import uploads_bp
    from src.routes.agents import agents_bp
    from src.routes.admin import admin_bp
    from src.routes.traders import traders_bp
    from src.routes.kyc import kyc_bp
    from src.routes.challenges import challenges_bp
    from src.routes.reports import reports_bp
    from src.routes.hierarchy import hierarchy_bp
    from src.routes.crm import crm_bp
    from src.routes.security import security_bp
    from src.routes.payment_approvals import bp as payment_approvals_bp
    from src.routes.chat import chat_bp
    from src.routes.tenants import tenants_bp
    from src.routes.roles import roles_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(users_bp, url_prefix='/api/v1/users')
    app.register_blueprint(profile_bp, url_prefix='/api/v1/profile')
    app.register_blueprint(programs_bp, url_prefix='/api/v1/programs')
    app.register_blueprint(payments_bp, url_prefix='/api/v1/payments')
    app.register_blueprint(uploads_bp, url_prefix='/api/v1/uploads')
    app.register_blueprint(agents_bp, url_prefix='/api/v1/agents')
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')
    app.register_blueprint(traders_bp, url_prefix='/api/v1/traders')
    app.register_blueprint(kyc_bp, url_prefix='/api/v1/kyc')
    app.register_blueprint(challenges_bp, url_prefix='/api/v1/challenges')
    app.register_blueprint(reports_bp, url_prefix='/api/v1/reports')
    app.register_blueprint(hierarchy_bp, url_prefix='/api/v1/hierarchy')
    app.register_blueprint(crm_bp, url_prefix='/api/v1/crm')
    app.register_blueprint(security_bp, url_prefix='/api/v1/security')
    app.register_blueprint(payment_approvals_bp)
    app.register_blueprint(chat_bp, url_prefix='/api/v1/chat')
    app.register_blueprint(tenants_bp, url_prefix='/api/v1/tenants')
    app.register_blueprint(roles_bp, url_prefix='/api/v1')
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'MarketEdgePros API',
            'version': '1.0.0'
        }), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'message': 'MarketEdgePros API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/health',
                'auth': '/api/v1/auth',
                'profile': '/api/v1/profile',
                'programs': '/api/v1/programs',
                'payments': '/api/v1/payments',
                'uploads': '/api/v1/uploads',
                'agents': '/api/v1/agents',
                'admin': '/api/v1/admin',
                'traders': '/api/v1/traders',
                'kyc': '/api/v1/kyc',
                'challenges': '/api/v1/challenges',
                'reports': '/api/v1/reports',
                'hierarchy': '/api/v1/hierarchy',
                'crm': '/api/v1/crm',
                'payment_approvals': '/api/v1/payment-approvals',
                'chat': '/api/v1/chat',
                'tenants': '/api/v1/tenants'
            }
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f'Unhandled exception: {str(error)}')
        return jsonify({'error': 'An unexpected error occurred'}), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

