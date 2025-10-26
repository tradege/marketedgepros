"""
Blog routes for public and admin access
"""
from flask import Blueprint, request, jsonify
from sqlalchemy import or_, desc
from src.database import db
from src.models.blog_post import BlogPost
from src.auth.decorators import token_required, admin_required
import logging

logger = logging.getLogger(__name__)

blog_bp = Blueprint('blog', __name__, url_prefix='/blog')


# ============================================================================
# PUBLIC ROUTES
# ============================================================================

@blog_bp.route('/posts', methods=['GET'])
def get_posts():
    """
    Get list of published blog posts
    Query params:
    - page: Page number (default: 1)
    - per_page: Posts per page (default: 10, max: 50)
    - category: Filter by category
    - featured: Filter featured posts (true/false)
    - sort: Sort by (latest, popular, oldest)
    """
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 50)
        category = request.args.get('category')
        featured = request.args.get('featured')
        sort = request.args.get('sort', 'latest')
        
        # Build query
        query = BlogPost.query.filter_by(status='published')
        
        # Apply filters
        if category:
            query = query.filter_by(category=category)
        
        if featured and featured.lower() == 'true':
            query = query.filter_by(featured=True)
        
        # Apply sorting
        if sort == 'popular':
            query = query.order_by(desc(BlogPost.view_count))
        elif sort == 'oldest':
            query = query.order_by(BlogPost.published_at.asc())
        else:  # latest (default)
            query = query.order_by(desc(BlogPost.published_at))
        
        # Paginate
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'posts': [post.to_dict_summary() for post in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_posts': pagination.total,
                'total_pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching blog posts: {str(e)}")
        return jsonify({'error': 'Failed to fetch blog posts'}), 500


@blog_bp.route('/posts/<slug>', methods=['GET'])
def get_post_by_slug(slug):
    """Get single blog post by slug"""
    try:
        post = BlogPost.query.filter_by(slug=slug, status='published').first()
        
        if not post:
            return jsonify({'error': 'Blog post not found'}), 404
        
        # Increment view count
        post.increment_views()
        
        return jsonify(post.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error fetching blog post: {str(e)}")
        return jsonify({'error': 'Failed to fetch blog post'}), 500


@blog_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get list of all categories with post counts"""
    try:
        # Get distinct categories from published posts
        categories_query = db.session.query(
            BlogPost.category,
            db.func.count(BlogPost.id).label('count')
        ).filter_by(status='published').group_by(BlogPost.category).all()
        
        categories = [
            {'name': cat, 'count': count}
            for cat, count in categories_query
        ]
        
        return jsonify({'categories': categories}), 200
        
    except Exception as e:
        logger.error(f"Error fetching categories: {str(e)}")
        return jsonify({'error': 'Failed to fetch categories'}), 500


@blog_bp.route('/search', methods=['GET'])
def search_posts():
    """
    Search blog posts
    Query params:
    - q: Search query (required)
    - page: Page number (default: 1)
    - per_page: Posts per page (default: 10)
    """
    try:
        query_text = request.args.get('q', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 50)
        
        if not query_text:
            return jsonify({'error': 'Search query is required'}), 400
        
        # Search in title, excerpt, and content
        search_filter = or_(
            BlogPost.title.ilike(f'%{query_text}%'),
            BlogPost.excerpt.ilike(f'%{query_text}%'),
            BlogPost.content.ilike(f'%{query_text}%'),
            BlogPost.tags.ilike(f'%{query_text}%')
        )
        
        # Build query
        query = BlogPost.query.filter_by(status='published').filter(search_filter)
        query = query.order_by(desc(BlogPost.published_at))
        
        # Paginate
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'posts': [post.to_dict_summary() for post in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_posts': pagination.total,
                'total_pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            },
            'query': query_text
        }), 200
        
    except Exception as e:
        logger.error(f"Error searching blog posts: {str(e)}")
        return jsonify({'error': 'Failed to search blog posts'}), 500


@blog_bp.route('/featured', methods=['GET'])
def get_featured_posts():
    """Get featured blog posts"""
    try:
        limit = min(request.args.get('limit', 3, type=int), 10)
        
        posts = BlogPost.query.filter_by(
            status='published',
            featured=True
        ).order_by(desc(BlogPost.published_at)).limit(limit).all()
        
        return jsonify({
            'posts': [post.to_dict_summary() for post in posts]
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching featured posts: {str(e)}")
        return jsonify({'error': 'Failed to fetch featured posts'}), 500


@blog_bp.route('/recent', methods=['GET'])
def get_recent_posts():
    """Get recent blog posts"""
    try:
        limit = min(request.args.get('limit', 5, type=int), 20)
        
        posts = BlogPost.query.filter_by(
            status='published'
        ).order_by(desc(BlogPost.published_at)).limit(limit).all()
        
        return jsonify({
            'posts': [post.to_dict_summary() for post in posts]
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching recent posts: {str(e)}")
        return jsonify({'error': 'Failed to fetch recent posts'}), 500


@blog_bp.route('/popular', methods=['GET'])
def get_popular_posts():
    """Get popular blog posts (by view count)"""
    try:
        limit = min(request.args.get('limit', 5, type=int), 20)
        
        posts = BlogPost.query.filter_by(
            status='published'
        ).order_by(desc(BlogPost.view_count)).limit(limit).all()
        
        return jsonify({
            'posts': [post.to_dict_summary() for post in posts]
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching popular posts: {str(e)}")
        return jsonify({'error': 'Failed to fetch popular posts'}), 500


# ============================================================================
# ADMIN ROUTES (Require Authentication)
# ============================================================================

@blog_bp.route('/admin/posts', methods=['GET'])
@token_required
@admin_required
def admin_get_all_posts(current_user):
    """Get all blog posts (including drafts) - Admin only"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        status = request.args.get('status')
        
        query = BlogPost.query
        
        if status:
            query = query.filter_by(status=status)
        
        query = query.order_by(desc(BlogPost.created_at))
        
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'posts': [post.to_dict() for post in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_posts': pagination.total,
                'total_pages': pagination.pages
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching admin posts: {str(e)}")
        return jsonify({'error': 'Failed to fetch posts'}), 500


@blog_bp.route('/admin/posts', methods=['POST'])
@token_required
@admin_required
def admin_create_post(current_user):
    """Create new blog post - Admin only"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'content', 'category']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Generate slug from title if not provided
        slug = data.get('slug') or BlogPost.generate_slug(data['title'])
        
        # Check if slug already exists
        if BlogPost.query.filter_by(slug=slug).first():
            return jsonify({'error': 'A post with this slug already exists'}), 400
        
        # Create new post
        post = BlogPost(
            title=data['title'],
            slug=slug,
            excerpt=data.get('excerpt'),
            content=data['content'],
            featured_image=data.get('featured_image'),
            featured_image_alt=data.get('featured_image_alt'),
            category=data['category'],
            tags=data.get('tags'),
            meta_title=data.get('meta_title'),
            meta_description=data.get('meta_description'),
            meta_keywords=data.get('meta_keywords'),
            author_id=current_user.id,
            status=data.get('status', 'draft'),
            featured=data.get('featured', False)
        )
        
        # Calculate reading time
        post.calculate_reading_time()
        
        # If status is published, set published_at
        if post.status == 'published' and not post.published_at:
            from datetime import datetime
            post.published_at = datetime.utcnow()
        
        db.session.add(post)
        db.session.commit()
        
        logger.info(f"Blog post created: {post.title} by user {current_user.id}")
        
        return jsonify({
            'message': 'Blog post created successfully',
            'post': post.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating blog post: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to create blog post'}), 500


@blog_bp.route('/admin/posts/<int:post_id>', methods=['PUT'])
@token_required
@admin_required
def admin_update_post(current_user, post_id):
    """Update blog post - Admin only"""
    try:
        post = BlogPost.query.get(post_id)
        
        if not post:
            return jsonify({'error': 'Blog post not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'title' in data:
            post.title = data['title']
        
        if 'slug' in data:
            # Check if new slug is unique
            existing = BlogPost.query.filter_by(slug=data['slug']).first()
            if existing and existing.id != post_id:
                return jsonify({'error': 'A post with this slug already exists'}), 400
            post.slug = data['slug']
        
        if 'excerpt' in data:
            post.excerpt = data['excerpt']
        
        if 'content' in data:
            post.content = data['content']
            post.calculate_reading_time()
        
        if 'featured_image' in data:
            post.featured_image = data['featured_image']
        
        if 'featured_image_alt' in data:
            post.featured_image_alt = data['featured_image_alt']
        
        if 'category' in data:
            post.category = data['category']
        
        if 'tags' in data:
            post.tags = data['tags']
        
        if 'meta_title' in data:
            post.meta_title = data['meta_title']
        
        if 'meta_description' in data:
            post.meta_description = data['meta_description']
        
        if 'meta_keywords' in data:
            post.meta_keywords = data['meta_keywords']
        
        if 'status' in data:
            old_status = post.status
            post.status = data['status']
            
            # If changing from draft to published, set published_at
            if old_status != 'published' and post.status == 'published':
                if not post.published_at:
                    from datetime import datetime
                    post.published_at = datetime.utcnow()
        
        if 'featured' in data:
            post.featured = data['featured']
        
        db.session.commit()
        
        logger.info(f"Blog post updated: {post.title} by user {current_user.id}")
        
        return jsonify({
            'message': 'Blog post updated successfully',
            'post': post.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error updating blog post: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to update blog post'}), 500


@blog_bp.route('/admin/posts/<int:post_id>', methods=['DELETE'])
@token_required
@admin_required
def admin_delete_post(current_user, post_id):
    """Delete blog post - Admin only"""
    try:
        post = BlogPost.query.get(post_id)
        
        if not post:
            return jsonify({'error': 'Blog post not found'}), 404
        
        title = post.title
        db.session.delete(post)
        db.session.commit()
        
        logger.info(f"Blog post deleted: {title} by user {current_user.id}")
        
        return jsonify({'message': 'Blog post deleted successfully'}), 200
        
    except Exception as e:
        logger.error(f"Error deleting blog post: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to delete blog post'}), 500


@blog_bp.route('/admin/posts/<int:post_id>/publish', methods=['POST'])
@token_required
@admin_required
def admin_publish_post(current_user, post_id):
    """Publish a blog post - Admin only"""
    try:
        post = BlogPost.query.get(post_id)
        
        if not post:
            return jsonify({'error': 'Blog post not found'}), 404
        
        post.publish()
        
        logger.info(f"Blog post published: {post.title} by user {current_user.id}")
        
        return jsonify({
            'message': 'Blog post published successfully',
            'post': post.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error publishing blog post: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to publish blog post'}), 500


@blog_bp.route('/admin/posts/<int:post_id>/unpublish', methods=['POST'])
@token_required
@admin_required
def admin_unpublish_post(current_user, post_id):
    """Unpublish a blog post - Admin only"""
    try:
        post = BlogPost.query.get(post_id)
        
        if not post:
            return jsonify({'error': 'Blog post not found'}), 404
        
        post.unpublish()
        
        logger.info(f"Blog post unpublished: {post.title} by user {current_user.id}")
        
        return jsonify({
            'message': 'Blog post unpublished successfully',
            'post': post.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error unpublishing blog post: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to unpublish blog post'}), 500

