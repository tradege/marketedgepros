"""
Hierarchical permissions system
Each role can see more data based on their position in the hierarchy
"""
from src.models.user import User
from sqlalchemy import or_, and_


class PermissionManager:
    """Manage hierarchical permissions"""
    
    # Role hierarchy (lower number = higher privileges)
    ROLE_HIERARCHY = {
        'admin': 0,           # Sees everything
        'supermaster': 1,     # Sees all downline
        'master': 2,          # Sees agents + traders below
        'agent': 3,           # Sees traders below
        'trader': 4,          # Sees only self
        'guest': 5            # Sees only public data
    }
    
    @staticmethod
    def get_role_level(role):
        """Get numeric level for role"""
        return PermissionManager.ROLE_HIERARCHY.get(role, 999)
    
    @staticmethod
    def can_view_user(viewer, target_user):
        """Check if viewer can see target_user's data"""
        
        # Admin can see everything
        if viewer.role == 'admin':
            return True
        
        # Can always see yourself
        if viewer.id == target_user.id:
            return True
        
        # Guest cannot see any user data
        if viewer.role == 'guest':
            return False
        
        # Trader can only see self
        if viewer.role == 'trader':
            return viewer.id == target_user.id
        
        # Check if target is in viewer's downline
        target_ancestors = target_user.get_ancestors()
        return viewer in target_ancestors
    
    @staticmethod
    def get_viewable_user_ids(user):
        """Get list of user IDs that this user can view"""
        
        # Admin sees all
        if user.role == 'admin':
            all_users = User.query.all()
            return [u.id for u in all_users]
        
        # Guest sees none
        if user.role == 'guest':
            return []
        
        # Trader sees only self
        if user.role == 'trader':
            return [user.id]
        
        # Others see self + all downline
        descendants = user.get_all_descendants()
        viewable_ids = [user.id] + [d.id for d in descendants]
        return viewable_ids
    
    @staticmethod
    def get_viewable_users_query(user):
        """Get SQLAlchemy query for users this user can view"""
        
        # Admin sees all
        if user.role == 'admin':
            return User.query
        
        # Guest sees none
        if user.role == 'guest':
            return User.query.filter(User.id == -1)  # No results
        
        # Trader sees only self
        if user.role == 'trader':
            return User.query.filter(User.id == user.id)
        
        # Others see self + downline using tree_path
        if user.tree_path:
            return User.query.filter(
                or_(
                    User.id == user.id,
                    User.tree_path.like(f"{user.tree_path}/%")
                )
            )
        else:
            return User.query.filter(User.id == user.id)
    
    @staticmethod
    def can_create_role(creator, target_role):
        """Check if creator can create a user with target_role"""
        
        # Admin can create anyone
        if creator.role == 'admin':
            return True
        
        # Guest and Trader cannot create users
        if creator.role in ['guest', 'trader']:
            return False
        
        # Check role hierarchy
        role_permissions = {
            'supermaster': ['supermaster', 'master', 'agent', 'trader'],
            'master': ['master', 'agent', 'trader'],
            'agent': ['agent', 'trader']
        }
        
        allowed_roles = role_permissions.get(creator.role, [])
        return target_role in allowed_roles
    
    @staticmethod
    def can_edit_user(editor, target_user):
        """Check if editor can modify target_user"""
        
        # Admin can edit anyone
        if editor.role == 'admin':
            return True
        
        # Can edit yourself (limited fields)
        if editor.id == target_user.id:
            return True
        
        # Guest and Trader cannot edit others
        if editor.role in ['guest', 'trader']:
            return editor.id == target_user.id
        
        # Can edit users in downline
        target_ancestors = target_user.get_ancestors()
        return editor in target_ancestors
    
    @staticmethod
    def can_delete_user(deleter, target_user):
        """Check if deleter can delete target_user"""
        
        # Admin can delete anyone
        if deleter.role == 'admin':
            return True
        
        # Cannot delete yourself
        if deleter.id == target_user.id:
            return False
        
        # Guest and Trader cannot delete
        if deleter.role in ['guest', 'trader']:
            return False
        
        # Can delete users in downline
        target_ancestors = target_user.get_ancestors()
        return deleter in target_ancestors
    
    @staticmethod
    def get_data_scope(user):
        """Get data scope description for user"""
        scopes = {
            'admin': 'all_system',
            'supermaster': 'all_downline',
            'master': 'downline_from_level',
            'agent': 'direct_traders',
            'trader': 'self_only',
            'guest': 'public_only'
        }
        return scopes.get(user.role, 'none')
    
    @staticmethod
    def filter_challenges_by_permission(user, query):
        """Filter challenges query based on user permissions"""
        from src.models.trading_program import Challenge
        
        # Admin sees all
        if user.role == 'admin':
            return query
        
        # Guest sees none
        if user.role == 'guest':
            return query.filter(Challenge.id == -1)
        
        # Trader sees only own
        if user.role == 'trader':
            return query.filter(Challenge.user_id == user.id)
        
        # Others see challenges of viewable users
        viewable_ids = PermissionManager.get_viewable_user_ids(user)
        return query.filter(Challenge.user_id.in_(viewable_ids))
    
    @staticmethod
    def filter_payments_by_permission(user, query):
        """Filter payments query based on user permissions"""
        from src.models.payment import Payment
        
        # Admin sees all
        if user.role == 'admin':
            return query
        
        # Guest sees none
        if user.role == 'guest':
            return query.filter(Payment.id == -1)
        
        # Trader sees only own
        if user.role == 'trader':
            return query.filter(Payment.user_id == user.id)
        
        # Others see payments of viewable users
        viewable_ids = PermissionManager.get_viewable_user_ids(user)
        return query.filter(Payment.user_id.in_(viewable_ids))
    
    @staticmethod
    def filter_withdrawals_by_permission(user, query):
        """Filter withdrawals query based on user permissions"""
        from src.models.withdrawal import Withdrawal
        
        # Admin sees all
        if user.role == 'admin':
            return query
        
        # Guest sees none
        if user.role == 'guest':
            return query.filter(Withdrawal.id == -1)
        
        # Trader sees only own
        if user.role == 'trader':
            return query.filter(Withdrawal.user_id == user.id)
        
        # Others see withdrawals of viewable users
        viewable_ids = PermissionManager.get_viewable_user_ids(user)
        return query.filter(Withdrawal.user_id.in_(viewable_ids))
    
    @staticmethod
    def filter_leads_by_permission(user, query):
        """Filter leads query based on user permissions"""
        from src.models.lead import Lead
        
        # Admin sees all
        if user.role == 'admin':
            return query
        
        # Guest sees none
        if user.role == 'guest':
            return query.filter(Lead.id == -1)
        
        # Trader sees none (traders don't manage leads)
        if user.role == 'trader':
            return query.filter(Lead.id == -1)
        
        # Others see leads assigned to them or their downline
        viewable_ids = PermissionManager.get_viewable_user_ids(user)
        return query.filter(
            or_(
                Lead.assigned_to.in_(viewable_ids),
                Lead.assigned_to == None  # Unassigned leads
            )
        )
    
    @staticmethod
    def get_dashboard_stats_scope(user):
        """Get which stats user can see on dashboard"""
        
        if user.role == 'admin':
            return {
                'users': 'all',
                'challenges': 'all',
                'payments': 'all',
                'withdrawals': 'all',
                'leads': 'all',
                'commissions': 'all'
            }
        
        if user.role == 'guest':
            return {
                'users': 'none',
                'challenges': 'none',
                'payments': 'none',
                'withdrawals': 'none',
                'leads': 'none',
                'commissions': 'none'
            }
        
        if user.role == 'trader':
            return {
                'users': 'self',
                'challenges': 'self',
                'payments': 'self',
                'withdrawals': 'self',
                'leads': 'none',
                'commissions': 'none'
            }
        
        # Agent, Master, SuperMaster
        return {
            'users': 'downline',
            'challenges': 'downline',
            'payments': 'downline',
            'withdrawals': 'downline',
            'leads': 'assigned',
            'commissions': 'downline'
        }
    
    @staticmethod
    def can_access_crm(user):
        """Check if user can access CRM features"""
        # Only agents and above can access CRM
        return user.role in ['admin', 'supermaster', 'master', 'agent']
    
    @staticmethod
    def can_manage_leads(user):
        """Check if user can manage leads"""
        return user.role in ['admin', 'supermaster', 'master', 'agent']
    
    @staticmethod
    def can_view_reports(user):
        """Check if user can view reports"""
        # Traders can only see their own reports
        # Others can see downline reports
        return user.role != 'guest'
    
    @staticmethod
    def can_approve_kyc(user):
        """Check if user can approve KYC"""
        # Only admin can approve KYC
        return user.role == 'admin'
    
    @staticmethod
    def can_manage_programs(user):
        """Check if user can manage trading programs"""
        # Only admin can manage programs
        return user.role == 'admin'
    
    @staticmethod
    def can_process_payments(user):
        """Check if user can process payments"""
        # Only admin can process payments
        return user.role == 'admin'
    
    @staticmethod
    def can_view_system_settings(user):
        """Check if user can view system settings"""
        return user.role == 'admin'
    
    @staticmethod
    def get_allowed_menu_items(user):
        """Get menu items user can access"""
        
        if user.role == 'guest':
            return ['home', 'programs', 'about', 'faq', 'contact']
        
        if user.role == 'trader':
            return [
                'home', 'programs', 'about', 'faq', 'contact',
                'dashboard', 'trading_history', 'withdrawals', 'documents', 'profile'
            ]
        
        if user.role in ['agent', 'master', 'supermaster']:
            return [
                'home', 'programs', 'about', 'faq', 'contact',
                'dashboard', 'my_team', 'crm', 'leads', 'commissions', 
                'reports', 'analytics', 'profile'
            ]
        
        if user.role == 'admin':
            return [
                'home', 'programs', 'about', 'faq', 'contact',
                'admin_dashboard', 'users', 'programs_mgmt', 'kyc_approval',
                'payments', 'settings', 'reports', 'analytics', 'crm', 'profile'
            ]
        
        return ['home']

