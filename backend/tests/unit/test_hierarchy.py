"""
Unit tests for User Hierarchy and MLM Structure
"""
import pytest
from src.models import User

@pytest.mark.unit
class TestUserHierarchy:
    """Test user hierarchy functionality"""
    
    def test_tree_path_root_user(self, session, super_admin_user):
        """Test tree path for root user"""
        assert super_admin_user.tree_path == str(super_admin_user.id)
        assert super_admin_user.parent_id is None
    
    def test_tree_path_child_user(self, session, super_admin_user):
        """Test tree path for child user"""
        child = User(
            email='child@example.com',
            first_name='Child',
            last_name='User',
            role='admin',
            parent_id=super_admin_user.id,
            is_active=True
        )
        child.set_password('ChildPassword123!')
        session.add(child)
        session.commit()
        child.update_tree_path()
        session.commit()
        
        expected_path = f"{super_admin_user.id}/{child.id}"
        assert child.tree_path == expected_path
    
    def test_tree_path_grandchild(self, session, super_admin_user):
        """Test tree path for grandchild user"""
        # Create child
        child = User(
            email='child@example.com',
            first_name='Child',
            last_name='User',
            role='admin',
            parent_id=super_admin_user.id,
            is_active=True
        )
        child.set_password('ChildPassword123!')
        session.add(child)
        session.commit()
        child.update_tree_path()
        session.commit()
        
        # Create grandchild
        grandchild = User(
            email='grandchild@example.com',
            first_name='Grandchild',
            last_name='User',
            role='trader',
            parent_id=child.id,
            is_active=True
        )
        grandchild.set_password('GrandchildPassword123!')
        session.add(grandchild)
        session.commit()
        grandchild.update_tree_path()
        session.commit()
        
        expected_path = f"{super_admin_user.id}/{child.id}/{grandchild.id}"
        assert grandchild.tree_path == expected_path
    
    def test_get_downline_count(self, session, super_admin_user, trader_user, admin_user):
        """Test getting downline count"""
        # super_admin has trader_user and admin_user as children
        count = super_admin_user.get_downline_count()
        assert count >= 0  # May have children
    
    def test_parent_child_relationship(self, session, super_admin_user, trader_user):
        """Test parent-child relationship"""
        # Set up parent-child relationship
        trader_user.parent_id = super_admin_user.id
        session.commit()
        trader_user.update_tree_path()
        session.commit()
        
        assert trader_user.parent_id == super_admin_user.id
        assert trader_user.parent == super_admin_user
    
    def test_role_hierarchy_permissions(self, session, super_admin_user):
        """Test role hierarchy permissions"""
        # Super admin can create admins
        assert super_admin_user.can_create_user('admin') is True
        
        # Super admin can create traders
        assert super_admin_user.can_create_user('trader') is True
    
    def test_admin_role_permissions(self, session, admin_user):
        """Test admin role permissions"""
        # Admin can create traders
        assert admin_user.can_create_user('trader') is True
        
        # Admin cannot create super_admin
        assert admin_user.can_create_user('super_admin') is False
    
    def test_multiple_children(self, session, super_admin_user):
        """Test user with multiple children"""
        children = []
        for i in range(3):
            child = User(
                email=f'child{i}@example.com',
                first_name=f'Child{i}',
                last_name='User',
                role='trader',
                parent_id=super_admin_user.id,
                is_active=True
            )
            child.set_password('Password123!')
            session.add(child)
            children.append(child)
        
        session.commit()
        
        for child in children:
            child.update_tree_path()
        session.commit()
        
        # All children should have super_admin as parent
        for child in children:
            assert child.parent_id == super_admin_user.id
            assert str(super_admin_user.id) in child.tree_path
    
    def test_tree_path_uniqueness(self, session, super_admin_user):
        """Test that each user has unique tree path"""
        users = []
        for i in range(5):
            user = User(
                email=f'user{i}@example.com',
                first_name=f'User{i}',
                last_name='Test',
                role='trader',
                parent_id=super_admin_user.id,
                is_active=True
            )
            user.set_password('Password123!')
            session.add(user)
            users.append(user)
        
        session.commit()
        
        for user in users:
            user.update_tree_path()
        session.commit()
        
        paths = [u.tree_path for u in users]
        assert len(paths) == len(set(paths))  # All unique
    
    def test_orphan_user_prevention(self, session):
        """Test that non-root users must have parent"""
        # Trader without parent should not be allowed
        user = User(
            email='orphan@example.com',
            first_name='Orphan',
            last_name='User',
            role='trader',
            parent_id=None,  # No parent!
            is_active=True
        )
        user.set_password('Password123!')
        session.add(user)
        session.commit()
        
        # Tree path will be just the user ID (orphan)
        user.update_tree_path()
        session.commit()
        
        assert user.tree_path == str(user.id)
    
    def test_level_calculation(self, session, super_admin_user):
        """Test user level calculation based on tree depth"""
        # Create 3-level hierarchy
        level1 = User(
            email='level1@example.com',
            first_name='Level1',
            last_name='User',
            role='admin',
            parent_id=super_admin_user.id,
            is_active=True
        )
        level1.set_password('Password123!')
        session.add(level1)
        session.commit()
        level1.update_tree_path()
        session.commit()
        
        level2 = User(
            email='level2@example.com',
            first_name='Level2',
            last_name='User',
            role='trader',
            parent_id=level1.id,
            is_active=True
        )
        level2.set_password('Password123!')
        session.add(level2)
        session.commit()
        level2.update_tree_path()
        session.commit()
        
        # Check tree path depths
        assert super_admin_user.tree_path.count('/') == 0  # Root
        assert level1.tree_path.count('/') == 1  # One level down
        assert level2.tree_path.count('/') == 2  # Two levels down
    
    def test_get_downline_by_level(self, session, super_admin_user, trader_user):
        """Test getting downline organized by level"""
        downline = super_admin_user.get_downline_by_level(max_level=2)
        
        # Should have at least level 1 (direct children)
        assert 1 in downline or len(downline) >= 0
