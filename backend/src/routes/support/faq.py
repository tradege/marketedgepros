"""
FAQ API Routes
"""
from flask import Blueprint, request, jsonify
from src.database import db
from src.models.support_ticket import FAQ
from src.utils.decorators import admin_required
import logging

logger = logging.getLogger(__name__)

faq_bp = Blueprint('support_faq', __name__)


# =====================================================
# Public Routes
# =====================================================

@faq_bp.route('/', methods=['GET'])
def get_faqs():
    """Get published FAQs"""
    try:
        category = request.args.get('category')
        featured_only = request.args.get('featured', 'false').lower() == 'true'
        
        query = FAQ.query.filter_by(is_published=True)
        
        if category:
            query = query.filter_by(category=category)
        
        if featured_only:
            query = query.filter_by(is_featured=True)
        
        faqs = query.order_by(FAQ.order.asc(), FAQ.created_at.desc()).all()
        
        return jsonify({
            'faqs': [faq.to_dict() for faq in faqs],
            'total': len(faqs)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching FAQs: {str(e)}")
        return jsonify({'error': 'Failed to fetch FAQs'}), 500


@faq_bp.route('/categories', methods=['GET'])
def get_faq_categories():
    """Get FAQ categories with counts"""
    try:
        categories = db.session.query(
            FAQ.category,
            db.func.count(FAQ.id).label('count')
        ).filter_by(is_published=True).group_by(FAQ.category).all()
        
        return jsonify({
            'categories': [{'name': cat, 'count': count} for cat, count in categories]
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching FAQ categories: {str(e)}")
        return jsonify({'error': 'Failed to fetch categories'}), 500


@faq_bp.route('/<int:faq_id>', methods=['GET'])
def get_faq(faq_id):
    """Get single FAQ and increment view count"""
    try:
        faq = FAQ.query.filter_by(id=faq_id, is_published=True).first()
        
        if not faq:
            return jsonify({'error': 'FAQ not found'}), 404
        
        # Increment view count
        faq.view_count += 1
        db.session.commit()
        
        return jsonify(faq.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error fetching FAQ: {str(e)}")
        return jsonify({'error': 'Failed to fetch FAQ'}), 500


@faq_bp.route('/<int:faq_id>/helpful', methods=['POST'])
def mark_faq_helpful(faq_id):
    """Mark FAQ as helpful or not helpful"""
    try:
        data = request.get_json()
        is_helpful = data.get('helpful', True)
        
        faq = FAQ.query.get(faq_id)
        if not faq:
            return jsonify({'error': 'FAQ not found'}), 404
        
        if is_helpful:
            faq.helpful_count += 1
        else:
            faq.not_helpful_count += 1
        
        db.session.commit()
        
        return jsonify({
            'message': 'Thank you for your feedback',
            'helpful_count': faq.helpful_count,
            'not_helpful_count': faq.not_helpful_count
        }), 200
        
    except Exception as e:
        logger.error(f"Error marking FAQ helpful: {str(e)}")
        return jsonify({'error': 'Failed to submit feedback'}), 500


# =====================================================
# Admin Routes
# =====================================================

@faq_bp.route('/admin', methods=['GET'])
@admin_required
def get_all_faqs(current_user):
    """Get all FAQs including unpublished (admin only)"""
    try:
        category = request.args.get('category')
        
        query = FAQ.query
        
        if category:
            query = query.filter_by(category=category)
        
        faqs = query.order_by(FAQ.order.asc(), FAQ.created_at.desc()).all()
        
        return jsonify({
            'faqs': [faq.to_dict() for faq in faqs],
            'total': len(faqs)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching FAQs: {str(e)}")
        return jsonify({'error': 'Failed to fetch FAQs'}), 500


@faq_bp.route('/admin', methods=['POST'])
@admin_required
def create_faq(current_user):
    """Create new FAQ"""
    try:
        data = request.get_json()
        
        question = data.get('question')
        answer = data.get('answer')
        category = data.get('category')
        
        if not question or not answer or not category:
            return jsonify({'error': 'Question, answer, and category are required'}), 400
        
        faq = FAQ(
            question=question,
            answer=answer,
            category=category,
            order=data.get('order', 0),
            is_featured=data.get('is_featured', False),
            is_published=data.get('is_published', True)
        )
        
        db.session.add(faq)
        db.session.commit()
        
        logger.info(f"FAQ created: {faq.id}")
        
        return jsonify({
            'message': 'FAQ created successfully',
            'faq': faq.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating FAQ: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to create FAQ'}), 500


@faq_bp.route('/admin/<int:faq_id>', methods=['PUT'])
@admin_required
def update_faq(current_user, faq_id):
    """Update FAQ"""
    try:
        data = request.get_json()
        
        faq = FAQ.query.get(faq_id)
        
        if not faq:
            return jsonify({'error': 'FAQ not found'}), 404
        
        # Update fields
        if 'question' in data:
            faq.question = data['question']
        if 'answer' in data:
            faq.answer = data['answer']
        if 'category' in data:
            faq.category = data['category']
        if 'order' in data:
            faq.order = data['order']
        if 'is_featured' in data:
            faq.is_featured = data['is_featured']
        if 'is_published' in data:
            faq.is_published = data['is_published']
        
        db.session.commit()
        
        logger.info(f"FAQ updated: {faq.id}")
        
        return jsonify({
            'message': 'FAQ updated successfully',
            'faq': faq.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error updating FAQ: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to update FAQ'}), 500


@faq_bp.route('/admin/<int:faq_id>', methods=['DELETE'])
@admin_required
def delete_faq(current_user, faq_id):
    """Delete FAQ"""
    try:
        faq = FAQ.query.get(faq_id)
        
        if not faq:
            return jsonify({'error': 'FAQ not found'}), 404
        
        db.session.delete(faq)
        db.session.commit()
        
        logger.info(f"FAQ deleted: {faq_id}")
        
        return jsonify({'message': 'FAQ deleted successfully'}), 200
        
    except Exception as e:
        logger.error(f"Error deleting FAQ: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to delete FAQ'}), 500

