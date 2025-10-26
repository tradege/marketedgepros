"""
Blog Post model for content management
"""
from src.database import db, TimestampMixin
from datetime import datetime
from sqlalchemy import Index


class BlogPost(db.Model, TimestampMixin):
    """Blog post model for content management"""
    
    __tablename__ = 'blog_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Content
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(250), unique=True, nullable=False, index=True)
    excerpt = db.Column(db.Text)  # Short summary
    content = db.Column(db.Text, nullable=False)  # Full HTML content
    
    # Media
    featured_image = db.Column(db.String(500))  # URL to featured image
    featured_image_alt = db.Column(db.String(200))  # Alt text for SEO
    
    # Categorization
    category = db.Column(db.String(50), nullable=False, index=True)
    # Categories: trading_strategies, risk_management, market_analysis, prop_trading, education, news
    tags = db.Column(db.String(500))  # Comma-separated tags
    
    # SEO
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.String(300))
    meta_keywords = db.Column(db.String(500))
    
    # Author & Publishing
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    status = db.Column(db.String(20), default='draft', nullable=False, index=True)
    # Status: draft, published, archived
    
    published_at = db.Column(db.DateTime, index=True)
    
    # Engagement
    view_count = db.Column(db.Integer, default=0)
    featured = db.Column(db.Boolean, default=False, index=True)  # Featured posts appear first
    
    # Reading time (in minutes)
    reading_time = db.Column(db.Integer, default=5)
    
    # Relationships
    author = db.relationship('User', backref='blog_posts')
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_blog_status_published', 'status', 'published_at'),
        Index('idx_blog_category_status', 'category', 'status'),
        Index('idx_blog_featured_status', 'featured', 'status'),
    )
    
    def __repr__(self):
        return f'<BlogPost {self.title}>'
    
    def publish(self):
        """Publish the blog post"""
        self.status = 'published'
        if not self.published_at:
            self.published_at = datetime.utcnow()
        db.session.commit()
    
    def unpublish(self):
        """Unpublish the blog post"""
        self.status = 'draft'
        db.session.commit()
    
    def archive(self):
        """Archive the blog post"""
        self.status = 'archived'
        db.session.commit()
    
    def increment_views(self):
        """Increment view count"""
        self.view_count += 1
        db.session.commit()
    
    def calculate_reading_time(self):
        """Calculate reading time based on content length"""
        if self.content:
            # Average reading speed: 200 words per minute
            word_count = len(self.content.split())
            self.reading_time = max(1, round(word_count / 200))
        return self.reading_time
    
    def get_tags_list(self):
        """Get tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def to_dict(self, include_content=True):
        """Convert blog post to dictionary"""
        data = {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'excerpt': self.excerpt,
            'featured_image': self.featured_image,
            'featured_image_alt': self.featured_image_alt,
            'category': self.category,
            'tags': self.get_tags_list(),
            'author': {
                'id': self.author.id,
                'name': f"{self.author.first_name} {self.author.last_name}",
                'email': self.author.email
            } if self.author else None,
            'status': self.status,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'view_count': self.view_count,
            'featured': self.featured,
            'reading_time': self.reading_time,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_content:
            data['content'] = self.content
            data['meta_title'] = self.meta_title
            data['meta_description'] = self.meta_description
            data['meta_keywords'] = self.meta_keywords
        
        return data
    
    def to_dict_summary(self):
        """Convert blog post to summary dictionary (without full content)"""
        return self.to_dict(include_content=False)
    
    @staticmethod
    def generate_slug(title):
        """Generate URL-friendly slug from title"""
        import re
        slug = title.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')

