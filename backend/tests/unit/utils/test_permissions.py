"""
Unit tests for Permissions System
Tests the hierarchical permissions and role-based access control
"""
import pytest
from src.models import User
from src.utils.permissions import PermissionManager


@pytest.mark.unit
class TestRoleHierarchy:
    """Test role hierarchy levels"""
    
    def test_role_hierarchy_levels(self):
        """Test that roles have correct hierarchy levels"""
        assert PermissionManager.get_role_level('admin') == 0
        assert PermissionManager.get_role_level('supermaster') == 1
        assert PermissionManager.get_role_level('master') == 2
        assert PermissionManager.get_role_level('agent') == 3
        assert PermissionManager.get_role_level('trader') == 4
        assert PermissionManager.get_role_level('guest') == 5
    
    def test_unknown_role_level(self):
        """Test that unknown roles get high level (low privilege)"""
        assert PermissionManager.get_role_level('unknown') == 999
        assert PermissionManager.get_role_level('') == 999
        assert PermissionManager.get_role_level(None) == 999
    
    def test_role_hierarchy_order(self):
        """Test that admin has highest privileges"""
        admin_level = PermissionManager.get_role_level('admin')
        trader_level = PermissionManager.get_role_level('trader')
        
        assert admin_level < trader_level  # Lower number = higher privilege


@pytest.mark.unit
class TestCanViewUser:
    """Test can_view_user permission checks"""
    
    def test_admin_can_view_anyone(self, session, super_admin_user, trader_user):
        """Test that admin can view any user"""
        super_admin_user.role = 'admin'
        
        assert PermissionManager.can_view_user(super_admin_user, trader_user) is True
    
    def test_user_can_view_self(self, session, trader_user):
        """Test that users can always view themselves"""
        assert PermissionManager.can_view_user(trader_user, trader_user) is True
    
    def test_guest_cannot_view_others(self, session, trader_user, admin_user):
        """Test that guest cannot view any user data"""
        trader_user.role = 'guest'
        
        assert PermissionManager.can_view_user(trader_user, admin_user) is False
    
    def test_trader_can_only_view_self(self, session):
        """Test that trader can only view themselves"""
        trader1 = User(
            email='trader1@test.com',
            first_name='Trader1',
            last_name='Test',
            role='trader',
            is_active=True
        )
        trader1.set_password('Password123!')
        
        trader2 = User(
            email='trader2@test.com',
            first_name='Trader2',
            last_name='Test',
            role='trader',
            is_active=True
        )
        trader2.set_password('Password123!')
        
        session.add_all([trader1, trader2])
        session.commit()
        
        # Trader can see self
        assert PermissionManager.can_view_user(trader1, trader1) is True
        
        # Trader cannot see other trader
        assert PermissionManager.can_view_user(trader1, trader2) is False
    
    def test_parent_can_view_child(self, session, super_admin_user):
        """Test that parent can view child in hierarchy"""
        child = User(
            email='child@test.com',
            first_name='Child',
            last_name='User',
            role='trader',
            parent_id=super_admin_user.id,
            is_active=True
        )
        child.set_password('Password123!')
        session.add(child)
        session.commit()
        child.update_tree_path()
        session.commit()
        
        # Parent can view child
        assert PermissionManager.can_view_user(super_admin_user, child) is True


@pytest.mark.unit
class TestGetViewableUserIds:
    """Test get_viewable_user_ids functionality"""
    
    def test_admin_sees_all_users(self, session, super_admin_user, trader_user):
        """Test that admin gets all user IDs"""
        super_admin_user.role = 'admin'
        
        viewable_ids = PermissionManager.get_viewable_user_ids(super_admin_user)
        
        assert super_admin_user.id in viewable_ids
        assert trader_user.id in viewable_ids
        assert len(viewable_ids) >= 2
    
    def test_guest_sees_no_users(self, session, trader_user):
        """Test that guest gets empty list"""
        trader_user.role = 'guest'
        
        viewable_ids = PermissionManager.get_viewable_user_ids(trader_user)
        
        assert viewable_ids == []
    
    def test_trader_sees_only_self(self, session, trader_user):
        """Test that trader sees only themselves"""
        viewable_ids = PermissionManager.get_viewable_user_ids(trader_user)
        
        assert viewable_ids == [trader_user.id]
    
    def test_parent_sees_self_and_downline(self, session, super_admin_user):
        """Test that parent sees self + all descendants"""
        # Create child
        child = User(
            email='child@test.com',
            first_name='Child',
            last_name='User',
            role='trader',
            parent_id=super_admin_user.id,
            is_active=True
        )
        child.set_password('Password123!')
        session.add(child)
        session.commit()
        child.update_tree_path()
        session.commit()
        
        viewable_ids = PermissionManager.get_viewable_user_ids(super_admin_user)
        
        assert super_admin_user.id in viewable_ids
        assert child.id in viewable_ids


@pytest.mark.unit
class TestGetViewableUsersQuery:
    """Test get_viewable_users_query functionality"""
    
    def test_admin_query_returns_all(self, session, super_admin_user):
        """Test that admin query returns all users"""
        super_admin_user.role = 'admin'
        
        query = PermissionManager.get_viewable_users_query(super_admin_user)
        users = query.all()
        
        assert len(users) >= 1
        assert super_admin_user in users
    
    def test_guest_query_returns_none(self, session, trader_user):
        """Test that guest query returns no users"""
        trader_user.role = 'guest'
        
        query = PermissionManager.get_viewable_users_query(trader_user)
        users = query.all()
        
        assert len(users) == 0
    
    def test_trader_query_returns_self(self, session, trader_user):
        """Test that trader query returns only self"""
        query = PermissionManager.get_viewable_users_query(trader_user)
        users = query.all()
        
        assert len(users) == 1
        assert users[0].id == trader_user.id
    
    def test_parent_query_includes_downline(self, session, super_admin_user):
        """Test that parent query includes downline"""
        # Create child
        child = User(
            email='child@test.com',
            first_name='Child',
            last_name='User',
            role='trader',
            parent_id=super_admin_user.id,
            is_active=True
        )
        child.set_password('Password123!')
        session.add(child)
        session.commit()
        child.update_tree_path()
        session.commit()
        
        query = PermissionManager.get_viewable_users_query(super_admin_user)
        users = query.all()
        
        user_ids = [u.id for u in users]
        assert super_admin_user.id in user_ids
        assert child.id in user_ids


@pytest.mark.unit
class TestCanCreateRole:
    """Test can_create_role permission checks"""
    
    def test_admin_can_create_any_role(self, session, super_admin_user):
        """Test that admin can create any role"""
        super_admin_user.role = 'admin'
        
        assert PermissionManager.can_create_role(super_admin_user, 'admin') is True
        assert PermissionManager.can_create_role(super_admin_user, 'supermaster') is True
        assert PermissionManager.can_create_role(super_admin_user, 'trader') is True
    
    def test_guest_cannot_create_users(self, session, trader_user):
        """Test that guest cannot create any users"""
        trader_user.role = 'guest'
        
        assert PermissionManager.can_create_role(trader_user, 'trader') is False
        assert PermissionManager.can_create_role(trader_user, 'guest') is False
    
    def test_trader_cannot_create_users(self, session, trader_user):
        """Test that trader cannot create any users"""
        assert PermissionManager.can_create_role(trader_user, 'trader') is False
        assert PermissionManager.can_create_role(trader_user, 'agent') is False
    
    def test_supermaster_can_create_downline_roles(self, session, super_admin_user):
        """Test that supermaster can create downline roles"""
        super_admin_user.role = 'supermaster'
        
        assert PermissionManager.can_create_role(super_admin_user, 'supermaster') is True
        assert PermissionManager.can_create_role(super_admin_user, 'master') is True
        assert PermissionManager.can_create_role(super_admin_user, 'agent') is True
        assert PermissionManager.can_create_role(super_admin_user, 'trader') is True
    
    def test_master_can_create_limited_roles(self, session, admin_user):
        """Test that master can create limited roles"""
        admin_user.role = 'master'
        
        assert PermissionManager.can_create_role(admin_user, 'master') is True
        assert PermissionManager.can_create_role(admin_user, 'agent') is True
        assert PermissionManager.can_create_role(admin_user, 'trader') is True
        assert PermissionManager.can_create_role(admin_user, 'supermaster') is False
    
    def test_agent_can_create_minimal_roles(self, session, admin_user):
        """Test that agent can create minimal roles"""
        admin_user.role = 'agent'
        
        assert PermissionManager.can_create_role(admin_user, 'agent') is True
        assert PermissionManager.can_create_role(admin_user, 'trader') is True
        assert PermissionManager.can_create_role(admin_user, 'master') is False


@pytest.mark.unit
class TestCanEditUser:
    """Test can_edit_user permission checks"""
    
    def test_admin_can_edit_anyone(self, session, super_admin_user, trader_user):
        """Test that admin can edit any user"""
        super_admin_user.role = 'admin'
        
        assert PermissionManager.can_edit_user(super_admin_user, trader_user) is True
    
    def test_user_can_edit_self(self, session, trader_user):
        """Test that users can edit themselves"""
        assert PermissionManager.can_edit_user(trader_user, trader_user) is True
    
    def test_guest_can_only_edit_self(self, session, trader_user, admin_user):
        """Test that guest can only edit themselves"""
        trader_user.role = 'guest'
        
        assert PermissionManager.can_edit_user(trader_user, trader_user) is True
        assert PermissionManager.can_edit_user(trader_user, admin_user) is False
    
    def test_trader_can_only_edit_self(self, session, trader_user, admin_user):
        """Test that trader can only edit themselves"""
        assert PermissionManager.can_edit_user(trader_user, trader_user) is True
        assert PermissionManager.can_edit_user(trader_user, admin_user) is False
    
    def test_parent_can_edit_child(self, session, super_admin_user):
        """Test that parent can edit child in hierarchy"""
        child = User(
            email='child@test.com',
            first_name='Child',
            last_name='User',
            role='trader',
            parent_id=super_admin_user.id,
            is_active=True
        )
        child.set_password('Password123!')
        session.add(child)
        session.commit()
        child.update_tree_path()
        session.commit()
        
        assert PermissionManager.can_edit_user(super_admin_user, child) is True


@pytest.mark.unit
class TestCanDeleteUser:
    """Test can_delete_user permission checks"""
    
    def test_admin_can_delete_anyone(self, session, super_admin_user, trader_user):
        """Test that admin can delete any user"""
        super_admin_user.role = 'admin'
        
        assert PermissionManager.can_delete_user(super_admin_user, trader_user) is True
    
    def test_cannot_delete_self(self, session, trader_user):
        """Test that users cannot delete themselves"""
        assert PermissionManager.can_delete_user(trader_user, trader_user) is False
    
    def test_guest_cannot_delete_anyone(self, session, trader_user, admin_user):
        """Test that guest cannot delete any user"""
        trader_user.role = 'guest'
        
        assert PermissionManager.can_delete_user(trader_user, admin_user) is False
        assert PermissionManager.can_delete_user(trader_user, trader_user) is False
    
    def test_trader_cannot_delete_anyone(self, session, trader_user, admin_user):
        """Test that trader cannot delete any user"""
        assert PermissionManager.can_delete_user(trader_user, admin_user) is False
        assert PermissionManager.can_delete_user(trader_user, trader_user) is False
    
    def test_parent_can_delete_child(self, session, super_admin_user):
        """Test that parent can delete child in hierarchy"""
        child = User(
            email='child@test.com',
            first_name='Child',
            last_name='User',
            role='trader',
            parent_id=super_admin_user.id,
            is_active=True
        )
        child.set_password('Password123!')
        session.add(child)
        session.commit()
        child.update_tree_path()
        session.commit()
        
        assert PermissionManager.can_delete_user(super_admin_user, child) is True


@pytest.mark.unit
class TestGetDataScope:
    """Test get_data_scope functionality"""
    
    def test_admin_data_scope(self, session, super_admin_user):
        """Test admin data scope"""
        super_admin_user.role = 'admin'
        scope = PermissionManager.get_data_scope(super_admin_user)
        
        assert scope == 'all_system'
    
    def test_supermaster_data_scope(self, session, super_admin_user):
        """Test supermaster data scope"""
        super_admin_user.role = 'supermaster'
        scope = PermissionManager.get_data_scope(super_admin_user)
        
        assert scope == 'all_downline'
    
    def test_master_data_scope(self, session, admin_user):
        """Test master data scope"""
        admin_user.role = 'master'
        scope = PermissionManager.get_data_scope(admin_user)
        
        assert scope == 'downline_from_level'
    
    def test_agent_data_scope(self, session, admin_user):
        """Test agent data scope"""
        admin_user.role = 'agent'
        scope = PermissionManager.get_data_scope(admin_user)
        
        assert scope == 'direct_traders'
    
    def test_trader_data_scope(self, session, trader_user):
        """Test trader data scope"""
        scope = PermissionManager.get_data_scope(trader_user)
        
        assert scope == 'self_only'
    
    def test_guest_data_scope(self, session, trader_user):
        """Test guest data scope"""
        trader_user.role = 'guest'
        scope = PermissionManager.get_data_scope(trader_user)
        
        assert scope == 'public_only'
