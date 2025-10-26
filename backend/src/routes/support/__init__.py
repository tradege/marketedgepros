"""
Support Module
Combines articles, tickets, and FAQ routes
"""
from flask import Blueprint

# Create main support blueprint
support_bp = Blueprint('support', __name__, url_prefix='/support')

# Import sub-modules
from .articles import articles_bp
from .tickets import tickets_bp
from .faq import faq_bp

# Register sub-blueprints
support_bp.register_blueprint(articles_bp, url_prefix='/articles')
support_bp.register_blueprint(tickets_bp, url_prefix='/tickets')
support_bp.register_blueprint(faq_bp, url_prefix='/faq')

__all__ = ['support_bp']

