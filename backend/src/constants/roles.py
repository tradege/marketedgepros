"""
Role constants for the application
Supports both old and new role naming conventions
"""

# Role definitions
class Roles:
    """Role constants"""
    SUPERMASTER = 'supermaster'
    SUPER_ADMIN = 'super_admin'
    MASTER = 'master'
    ADMIN = 'admin'
    AGENT = 'agent'
    TRADER = 'trader'
    GUEST = 'guest'
    
    # All admin roles (can access admin panel and create users)
    # Note: AGENT is NOT included - agents use referral codes, not direct user creation
    ADMIN_ROLES = [SUPERMASTER, SUPER_ADMIN, MASTER, ADMIN]
    
    # All supermaster roles (highest level)
    SUPERMASTER_ROLES = [SUPERMASTER, SUPER_ADMIN]
    
    # All master roles
    MASTER_ROLES = [MASTER, ADMIN]
    
    # All roles
    ALL_ROLES = [SUPERMASTER, SUPER_ADMIN, MASTER, ADMIN, AGENT, TRADER, GUEST]
    
    @staticmethod
    def is_admin(role):
        """Check if role is admin level"""
        return role in Roles.ADMIN_ROLES
    
    @staticmethod
    def is_supermaster(role):
        """Check if role is supermaster level"""
        return role in Roles.SUPERMASTER_ROLES
    
    @staticmethod
    def is_master(role):
        """Check if role is master level"""
        return role in Roles.MASTER_ROLES
    
    @staticmethod
    def normalize_role(role):
        """Normalize role to new naming convention"""
        role_mapping = {
            'super_admin': 'supermaster',
            'admin': 'master',
        }
        return role_mapping.get(role, role)
    
    @staticmethod
    def get_display_name(role):
        """Get display name for role"""
        display_names = {
            'supermaster': 'Super Admin',
            'super_admin': 'Super Admin',
            'master': 'Master',
            'admin': 'Admin',
            'agent': 'Agent',
            'trader': 'Trader',
            'guest': 'Guest',
        }
        return display_names.get(role, role.title())


# Role hierarchy for user creation permissions
ROLE_HIERARCHY = {
    'supermaster': ['supermaster', 'super_admin', 'master', 'admin', 'agent', 'trader', 'guest'],
    'super_admin': ['supermaster', 'super_admin', 'master', 'admin', 'agent', 'trader', 'guest'],
    'master': ['master', 'admin', 'agent', 'trader', 'guest'],
    'admin': ['master', 'admin', 'agent', 'trader', 'guest'],
    'agent': ['agent', 'trader', 'guest'],
    'trader': [],
    'guest': []
}

