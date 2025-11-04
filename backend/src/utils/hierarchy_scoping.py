"""
Centralized Hierarchy Filtering System

This module provides automatic hierarchy-based filtering for all SQLAlchemy queries.
Add HierarchyScopedMixin to any model that should be filtered by user hierarchy.

Usage:
    1. Add mixin to model: class User(db.Model, HierarchyScopedMixin)
    2. Initialize in app: init_hierarchy_scoping(db, User)
    3. Set scope in auth: set_request_hierarchy_scope(db.session, current_user)
    4. All queries are now automatically filtered!

Author: Manus AI
Date: October 25, 2025
"""

from sqlalchemy import event, inspect
from sqlalchemy.orm import with_loader_criteria
from flask import g, has_request_context


class HierarchyScopedMixin:
    """
    Add this mixin to any model that should be filtered by hierarchy.
    
    Requirements:
    - Model must have a relationship to User (directly or indirectly)
    - Override __hierarchy_user_fk__ if FK is not 'user_id'
    
    Example:
        class Withdrawal(db.Model, HierarchyScopedMixin):
            __hierarchy_user_fk__ = 'user_id'  # Default
            ...
        
        class Commission(db.Model, HierarchyScopedMixin):
            __hierarchy_user_fk__ = 'agent_id'  # Custom FK
            ...
    """
    
    __hierarchy_user_fk__ = 'user_id'  # Override in model if different
    
    @classmethod
    def hierarchy_filter_for_entity(cls, current_user):
        """
        Returns the filter condition for this model.
        Override for custom logic.
        
        Args:
            current_user: The current logged-in user
            
        Returns:
            SQLAlchemy filter condition or None (if supermaster)
        """
        from src.models.user import User
        
        # Supermaster sees everything
        if current_user.role == 'supermaster':
            return None
        
        # Get FK column name
        fk_col = getattr(cls, cls.__hierarchy_user_fk__)
        
        # Filter: user_id IN (SELECT id FROM users WHERE tree_path LIKE 'current_user_path%')
        # FIXED: Escape special characters to prevent SQL injection
        from sqlalchemy import func
        safe_tree_path = current_user.tree_path.replace("%", "\\%").replace("_", "\\_")
        return fk_col.in_(
            User.query.filter(
                User.tree_path.like(f"{safe_tree_path}%", escape="\\")
            ).with_entities(User.id)
        )


def set_request_hierarchy_scope(session, current_user):
    """
    Set the hierarchy scope for the current request.
    Call this in your auth decorator after loading the current user.
    
    Args:
        session: SQLAlchemy session
        current_user: The current logged-in user
        
    Example:
        @token_required
        def decorated(*args, **kwargs):
            current_user = User.query.get(user_id)
            set_request_hierarchy_scope(db.session, current_user)
            return f(*args, **kwargs)
    """
    if has_request_context():
        g.hierarchy_scope_user = current_user
        # Store user data to avoid accessing current_user object in Event Hook
        g.hierarchy_scope_role = getattr(current_user, 'role', None)
        g.hierarchy_scope_tree_path = getattr(current_user, 'tree_path', None)
        g.hierarchy_scope_parent_id = getattr(current_user, 'parent_id', None)
        g.hierarchy_scope_enabled = True


def without_hierarchy_scope(session):
    """
    Context manager to temporarily disable hierarchy scoping.
    Use this for admin reports or operations that need ALL data.
    
    Args:
        session: SQLAlchemy session
        
    Returns:
        Context manager
        
    Example:
        with without_hierarchy_scope(db.session):
            all_users = User.query.all()  # Gets ALL users, bypassing hierarchy
    """
    class _ScopeDisabler:
        def __enter__(self):
            if has_request_context():
                self._previous_state = getattr(g, 'hierarchy_scope_enabled', True)
                g.hierarchy_scope_enabled = False
            return self
        
        def __exit__(self, *args):
            if has_request_context():
                g.hierarchy_scope_enabled = getattr(self, '_previous_state', True)
    
    return _ScopeDisabler()


def init_hierarchy_scoping(db, user_model):
    """
    Initialize the hierarchy scoping system.
    Call this ONCE during app startup.
    
    This sets up SQLAlchemy event listeners that intercept ALL queries
    and automatically apply hierarchy filtering.
    
    Args:
        db: SQLAlchemy database instance
        user_model: User model class
        
    Example:
        def create_app():
            app = Flask(__name__)
            db.init_app(app)
            
            with app.app_context():
                init_hierarchy_scoping(db, User)
            
            return app
    """
    
    @event.listens_for(db.session, "do_orm_execute")
    def _apply_hierarchy_scope(execute_state):
        """
        This event fires for EVERY ORM query.
        We intercept and add hierarchy filtering automatically.
        
        This is the MAGIC that makes everything work!
        """
        
        # Skip if not in request context
        if not has_request_context():
            return
        
        # Skip if scoping is disabled
        if not getattr(g, 'hierarchy_scope_enabled', False):
            return
        
        # Skip if no current user data
        role_value = getattr(g, 'hierarchy_scope_role', None)
        tree_path = getattr(g, 'hierarchy_scope_tree_path', None)
        parent_id = getattr(g, 'hierarchy_scope_parent_id', None)
        
        if not role_value or not tree_path:
            return
        
        # Skip if ROOT supermaster (parent_id=None) - sees everything
        # Created supermasters (parent_id != None) are filtered like others
        if role_value == 'supermaster' and parent_id is None:
            return
        
        # Skip if explicitly bypassed
        if execute_state.execution_options.get('skip_hierarchy_scope', False):
            return
        
        # Check if this is a SELECT statement
        if not hasattr(execute_state.statement, 'column_descriptions'):
            return
        
        # Apply filtering to each entity in the query
        for entity in execute_state.statement.column_descriptions:
            model = entity.get('entity')
            
            # Skip if not a model or doesn't have the mixin
            if not model or not isinstance(model, type):
                continue
            
            if not issubclass(model, HierarchyScopedMixin):
                continue
            
            # Get the filter for this model
            # Create a simple object with tree_path, role, and parent_id to avoid accessing current_user
            class _ScopeData:
                def __init__(self, tree_path, role, parent_id):
                    self.tree_path = tree_path
                    self.role = role
                    self.parent_id = parent_id
            
            scope_data = _ScopeData(tree_path, role_value, parent_id)
            filter_condition = model.hierarchy_filter_for_entity(scope_data)
            
            if filter_condition is not None:
                # Apply the filter using with_loader_criteria
                execute_state.statement = execute_state.statement.options(
                    with_loader_criteria(
                        model,
                        filter_condition,
                        include_aliases=True
                    )
                )


# Utility function for explicit bypass using execution_options
def unscoped_query(query):
    """
    Bypass hierarchy scoping for a specific query.
    
    Args:
        query: SQLAlchemy query object
        
    Returns:
        Query with hierarchy scoping disabled
        
    Example:
        all_users = unscoped_query(User.query).all()
    """
    return query.execution_options(skip_hierarchy_scope=True)

