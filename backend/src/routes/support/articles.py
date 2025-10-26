"""
Support Articles API Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.database import db
from src.models.support_article import SupportArticle
from src.models.user import User
from src.constants.roles import ADMIN_ROLES
import logging
from slugify import slugify

logger = logging.getLogger(__name__)

articles_bp = Blueprint('support_articles', __name__)


@articles_bp.route('/', methods=['GET'])
def get_articles():
    """
    Get all published support articles
    Query params: category, search, featured
    """
    try:
        query = SupportArticle.query.filter_by(status='published')
        
        # Filter by category
        category = request.args.get('category')
        if category and category != 'all':
            query = query.filter_by(category=category)
        
        # Search
        search = request.args.get('search')
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                db.or_(
                    SupportArticle.title.ilike(search_term),
                    SupportArticle.content.ilike(search_term),
                    SupportArticle.excerpt.ilike(search_term)
                )
            )
        
        # Featured only
        featured = request.args.get('featured')
        if featured == 'true':
            query = query.filter_by(featured=True)
        
        # Order by featured first, then by order, then by date
        articles = query.order_by(
            SupportArticle.featured.desc(),
            SupportArticle.order.asc(),
            SupportArticle.published_at.desc()
        ).all()
        
        return jsonify({
            'articles': [article.to_dict(include_content=False) for article in articles],
            'total': len(articles)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching articles: {str(e)}")
        return jsonify({'error': 'Failed to fetch articles'}), 500


@articles_bp.route('/<slug>', methods=['GET'])
def get_article(slug):
    """Get single article by slug"""
    try:
        article = SupportArticle.query.filter_by(slug=slug, status='published').first()
        
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        
        # Increment view count
        article.increment_views()
        
        return jsonify(article.to_dict(include_content=True)), 200
        
    except Exception as e:
        logger.error(f"Error fetching article: {str(e)}")
        return jsonify({'error': 'Failed to fetch article'}), 500


@articles_bp.route('/<int:article_id>/feedback', methods=['POST'])
def article_feedback(article_id):
    """Mark article as helpful or not helpful"""
    try:
        data = request.get_json()
        helpful = data.get('helpful', True)
        
        article = SupportArticle.query.get(article_id)
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        
        article.mark_helpful(helpful)
        
        return jsonify({
            'message': 'Feedback recorded',
            'helpful_count': article.helpful_count,
            'not_helpful_count': article.not_helpful_count
        }), 200
        
    except Exception as e:
        logger.error(f"Error recording feedback: {str(e)}")
        return jsonify({'error': 'Failed to record feedback'}), 500


@articles_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all article categories with counts"""
    try:
        categories = db.session.query(
            SupportArticle.category,
            db.func.count(SupportArticle.id).label('count')
        ).filter_by(status='published').group_by(SupportArticle.category).all()
        
        return jsonify({
            'categories': [
                {'name': cat[0], 'count': cat[1]}
                for cat in categories
            ]
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching categories: {str(e)}")
        return jsonify({'error': 'Failed to fetch categories'}), 500


# Admin routes
@articles_bp.route('/admin', methods=['POST'])
@jwt_required()
def create_article():
    """Create new support article (Admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role not in ADMIN_ROLES:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        # Generate slug from title
        slug = slugify(data.get('title'))
        
        # Check if slug already exists
        existing = SupportArticle.query.filter_by(slug=slug).first()
        if existing:
            slug = f"{slug}-{SupportArticle.query.count() + 1}"
        
        article = SupportArticle(
            title=data.get('title'),
            slug=slug,
            content=data.get('content'),
            excerpt=data.get('excerpt'),
            category=data.get('category'),
            subcategory=data.get('subcategory'),
            tags=data.get('tags', []),
            meta_description=data.get('meta_description'),
            meta_keywords=data.get('meta_keywords'),
            status=data.get('status', 'draft'),
            author_id=user_id,
            featured=data.get('featured', False),
            order=data.get('order', 0)
        )
        
        if article.status == 'published' and not article.published_at:
            from datetime import datetime
            article.published_at = datetime.utcnow()
        
        db.session.add(article)
        db.session.commit()
        
        return jsonify({
            'message': 'Article created successfully',
            'article': article.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating article: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to create article'}), 500


@articles_bp.route('/admin/<int:article_id>', methods=['PUT'])
@jwt_required()
def update_article(article_id):
    """Update support article (Admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role not in ADMIN_ROLES:
            return jsonify({'error': 'Unauthorized'}), 403
        
        article = SupportArticle.query.get(article_id)
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'title' in data:
            article.title = data['title']
            article.slug = slugify(data['title'])
        
        if 'content' in data:
            article.content = data['content']
        
        if 'excerpt' in data:
            article.excerpt = data['excerpt']
        
        if 'category' in data:
            article.category = data['category']
        
        if 'subcategory' in data:
            article.subcategory = data['subcategory']
        
        if 'tags' in data:
            article.tags = data['tags']
        
        if 'meta_description' in data:
            article.meta_description = data['meta_description']
        
        if 'meta_keywords' in data:
            article.meta_keywords = data['meta_keywords']
        
        if 'status' in data:
            old_status = article.status
            article.status = data['status']
            
            # Set published_at when publishing
            if old_status != 'published' and data['status'] == 'published':
                from datetime import datetime
                article.published_at = datetime.utcnow()
        
        if 'featured' in data:
            article.featured = data['featured']
        
        if 'order' in data:
            article.order = data['order']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Article updated successfully',
            'article': article.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error updating article: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to update article'}), 500


@articles_bp.route('/admin/<int:article_id>', methods=['DELETE'])
@jwt_required()
def delete_article(article_id):
    """Delete support article (Admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role not in ADMIN_ROLES:
            return jsonify({'error': 'Unauthorized'}), 403
        
        article = SupportArticle.query.get(article_id)
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        
        db.session.delete(article)
        db.session.commit()
        
        return jsonify({'message': 'Article deleted successfully'}), 200
        
    except Exception as e:
        logger.error(f"Error deleting article: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to delete article'}), 500

