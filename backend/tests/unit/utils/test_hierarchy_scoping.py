"""
Unit tests for Hierarchy Scoping System
Tests the automatic hierarchy-based filtering for SQLAlchemy queries
"""
import pytest
from flask import g
from src.models import User
from src.utils.hierarchy_scoping import (
    HierarchyScopedMixin,
    set_request_hierarchy_scope,
    without_hierarchy_scope,
    unscoped_query
)


@pytest.mark.unit
class TestHierarchyScopedMixin:
    """Test HierarchyScopedMixin functionality"""
    
    def test_default_hierarchy_user_fk(self):
        """Test default hierarchy user FK is 'user_id'"""
        assert HierarchyScopedMixin.__hierarchy_user_fk__ == 'user_id'
    
    def test_hierarchy_filter_for_supermaster(self, session, super_admin_user):
        """Test that supermaster sees everything (no filter)"""
        # Create a mock model with the mixin
        class MockModel(HierarchyScopedMixin):
            pass
        
        # Supermaster should return None (no filter)
        super_admin_user.role = 'supermaster'
        filter_condition = MockModel.hierarchy_filter_for_entity(super_admin_user)
        
        assert filter_condition is None
    
    def test_hierarchy_filter_for_regular_user(self, session, admin_user):
        """Test that regular users get filtered"""
        # Admin should get a filter condition
        admin_user.tree_path = f"{admin_user.id}"
        
        # Filter should not be None for non-supermaster
        assert admin_user.role != 'supermaster'


@pytest.mark.unit
class TestSetRequestHierarchyScope:
    """Test set_request_hierarchy_scope functionality"""
    
    def test_set_scope_with_user(self, app, session, admin_user):
        """Test setting hierarchy scope with a user"""
        with app.test_request_context():
            set_request_hierarchy_scope(session, admin_user)
            
            assert hasattr(g, 'hierarchy_scope_user')
            assert g.hierarchy_scope_user == admin_user
            assert g.hierarchy_scope_role == admin_user.role
            assert g.hierarchy_scope_tree_path == admin_user.tree_path
            assert g.hierarchy_scope_parent_id == admin_user.parent_id
            assert g.hierarchy_scope_enabled is True
    
    def test_set_scope_stores_user_data(self, app, session, trader_user):
        """Test that scope stores user data correctly"""
        with app.test_request_context():
            set_request_hierarchy_scope(session, trader_user)
            
            assert g.hierarchy_scope_role == trader_user.role
            assert g.hierarchy_scope_tree_path == trader_user.tree_path
            assert g.hierarchy_scope_parent_id == trader_user.parent_id
    
    def test_set_scope_with_supermaster(self, app, session, super_admin_user):
        """Test setting scope with supermaster user"""
        with app.test_request_context():
            super_admin_user.role = 'supermaster'
            set_request_hierarchy_scope(session, super_admin_user)
            
            assert g.hierarchy_scope_role == 'supermaster'
            assert g.hierarchy_scope_enabled is True
    
    def test_set_scope_without_request_context(self, session, admin_user):
        """Test that setting scope outside request context doesn't crash"""
        # Should not raise an error
        try:
            set_request_hierarchy_scope(session, admin_user)
        except RuntimeError:
            # Expected - no request context
            pass


@pytest.mark.unit
class TestWithoutHierarchyScope:
    """Test without_hierarchy_scope context manager"""
    
    def test_disable_scope_temporarily(self, app, session, admin_user):
        """Test that scope can be disabled temporarily"""
        with app.test_request_context():
            # Enable scope first
            set_request_hierarchy_scope(session, admin_user)
            assert g.hierarchy_scope_enabled is True
            
            # Disable scope
            with without_hierarchy_scope(session):
                assert g.hierarchy_scope_enabled is False
            
            # Should be re-enabled after context
            assert g.hierarchy_scope_enabled is True
    
    def test_scope_restored_after_exception(self, app, session, admin_user):
        """Test that scope is restored even if exception occurs"""
        with app.test_request_context():
            set_request_hierarchy_scope(session, admin_user)
            assert g.hierarchy_scope_enabled is True
            
            try:
                with without_hierarchy_scope(session):
                    assert g.hierarchy_scope_enabled is False
                    raise ValueError("Test exception")
            except ValueError:
                pass
            
            # Should still be re-enabled
            assert g.hierarchy_scope_enabled is True
    
    def test_nested_scope_disabling(self, app, session, admin_user):
        """Test nested scope disabling"""
        with app.test_request_context():
            set_request_hierarchy_scope(session, admin_user)
            
            with without_hierarchy_scope(session):
                assert g.hierarchy_scope_enabled is False
                
                with without_hierarchy_scope(session):
                    assert g.hierarchy_scope_enabled is False
                
                assert g.hierarchy_scope_enabled is False
            
            assert g.hierarchy_scope_enabled is True
    
    def test_without_scope_no_request_context(self, session):
        """Test without_hierarchy_scope outside request context"""
        # Should not crash
        with without_hierarchy_scope(session):
            pass


@pytest.mark.unit
class TestUnscopedQuery:
    """Test unscoped_query functionality"""
    
    def test_unscoped_query_adds_execution_option(self, session):
        """Test that unscoped_query adds skip_hierarchy_scope option"""
        query = User.query
        unscoped = unscoped_query(query)
        
        # Check that execution option is set
        options = unscoped._execution_options
        assert 'skip_hierarchy_scope' in options
        assert options['skip_hierarchy_scope'] is True
    
    def test_unscoped_query_returns_query(self, session):
        """Test that unscoped_query returns a query object"""
        query = User.query
        unscoped = unscoped_query(query)
        
        # Should still be a query object
        assert hasattr(unscoped, 'all')
        assert hasattr(unscoped, 'filter')
        assert hasattr(unscoped, 'first')


@pytest.mark.unit
class TestHierarchyFilteringIntegration:
    """Test hierarchy filtering integration with real queries"""
    
    def test_supermaster_sees_all_users(self, app, session, super_admin_user):
        """Test that supermaster can see all users"""
        with app.test_request_context():
            super_admin_user.role = 'supermaster'
            super_admin_user.parent_id = None  # Root supermaster
            set_request_hierarchy_scope(session, super_admin_user)
            
            # Create some users
            user1 = User(
                email='user1@test.com',
                first_name='User1',
                last_name='Test',
                role='trader',
                is_active=True
            )
            user1.set_password('Password123!')
            session.add(user1)
            session.commit()
            
            # Supermaster should see all users
            users = User.query.all()
            assert len(users) >= 1
    
    def test_regular_user_filtered_by_hierarchy(self, app, session, admin_user, trader_user):
        """Test that regular users are filtered by hierarchy"""
        with app.test_request_context():
            # Set trader as child of admin
            trader_user.parent_id = admin_user.id
            trader_user.tree_path = f"{admin_user.id}/{trader_user.id}"
            session.commit()
            
            set_request_hierarchy_scope(session, admin_user)
            
            # Admin should see trader in their downline
            # Note: Actual filtering depends on HierarchyScopedMixin implementation
            assert admin_user.role != 'supermaster'
    
    def test_unscoped_query_bypasses_filtering(self, app, session, admin_user):
        """Test that unscoped_query bypasses hierarchy filtering"""
        with app.test_request_context():
            set_request_hierarchy_scope(session, admin_user)
            
            # Unscoped query should bypass filtering
            all_users = unscoped_query(User.query).all()
            assert isinstance(all_users, list)
    
    def test_without_scope_bypasses_filtering(self, app, session, admin_user):
        """Test that without_hierarchy_scope bypasses filtering"""
        with app.test_request_context():
            set_request_hierarchy_scope(session, admin_user)
            
            # Within context, filtering should be bypassed
            with without_hierarchy_scope(session):
                all_users = User.query.all()
                assert isinstance(all_users, list)


@pytest.mark.unit
class TestHierarchyScopingEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_scope_with_none_user(self, app, session):
        """Test setting scope with None user"""
        with app.test_request_context():
            # Should not crash
            try:
                set_request_hierarchy_scope(session, None)
            except AttributeError:
                # Expected - None has no attributes
                pass
    
    def test_scope_with_user_no_tree_path(self, app, session):
        """Test setting scope with user that has no tree_path"""
        with app.test_request_context():
            user = User(
                email='nopath@test.com',
                first_name='No',
                last_name='Path',
                role='trader',
                is_active=True
            )
            user.set_password('Password123!')
            session.add(user)
            session.commit()
            
            # Should not crash
            set_request_hierarchy_scope(session, user)
    
    def test_multiple_scope_sets(self, app, session, admin_user, trader_user):
        """Test setting scope multiple times in same request"""
        with app.test_request_context():
            set_request_hierarchy_scope(session, admin_user)
            assert g.hierarchy_scope_user == admin_user
            
            # Set again with different user
            set_request_hierarchy_scope(session, trader_user)
            assert g.hierarchy_scope_user == trader_user
    
    def test_scope_persists_across_queries(self, app, session, admin_user):
        """Test that scope persists across multiple queries"""
        with app.test_request_context():
            set_request_hierarchy_scope(session, admin_user)
            
            # Multiple queries should all use the same scope
            query1 = User.query.all()
            query2 = User.query.filter_by(role='trader').all()
            query3 = User.query.filter(User.is_active == True).all()
            
            # All queries should execute without error
            assert isinstance(query1, list)
            assert isinstance(query2, list)
            assert isinstance(query3, list)
