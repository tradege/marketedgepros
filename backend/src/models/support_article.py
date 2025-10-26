"""
Support Article Model
"""
from datetime import datetime
from ..extensions import db


class SupportArticle(db.Model):
    """Support knowledge base articles"""
    __tablename__ = 'support_articles'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(500))
    
    # Category & Organization
    category = db.Column(db.String(100), nullable=False, index=True)
    subcategory = db.Column(db.String(100))
    tags = db.Column(db.JSON)  # Array of tags
    
    # SEO
    meta_description = db.Column(db.String(160))
    meta_keywords = db.Column(db.String(255))
    
    # Status & Publishing
    status = db.Column(db.String(20), default='draft', nullable=False)  # draft, published, archived
    published_at = db.Column(db.DateTime)
    
    # Author
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', backref='support_articles')
    
    # Engagement
    views = db.Column(db.Integer, default=0)
    helpful_count = db.Column(db.Integer, default=0)
    not_helpful_count = db.Column(db.Integer, default=0)
    
    # Ordering
    order = db.Column(db.Integer, default=0)
    featured = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self, include_content=True):
        data = {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'excerpt': self.excerpt,
            'category': self.category,
            'subcategory': self.subcategory,
            'tags': self.tags or [],
            'status': self.status,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'views': self.views,
            'helpful_count': self.helpful_count,
            'not_helpful_count': self.not_helpful_count,
            'featured': self.featured,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_content:
            data['content'] = self.content
        
        if self.author:
            data['author'] = {
                'id': self.author.id,
                'name': f"{self.author.first_name} {self.author.last_name}"
            }
        
        return data
    
    def increment_views(self):
        """Increment view count"""
        self.views += 1
        db.session.commit()
    
    def mark_helpful(self, helpful=True):
        """Mark article as helpful or not helpful"""
        if helpful:
            self.helpful_count += 1
        else:
            self.not_helpful_count += 1
        db.session.commit()

