"""
Role constants for the application - FIXED VERSION
Supports proper hierarchy as per requirements
"""

# Role definitions
class Roles:
    """Role constants"""
    SUPERMASTER = 'supermaster'
    MASTER = 'master'
    AFFILIATE = 'affiliate'  # Changed from AGENT
    TRADER = 'trader'
    GUEST = 'guest'
    
    # All admin roles (can access admin panel)
    ADMIN_ROLES = [SUPERMASTER, MASTER]
    
    # All supermaster roles (highest level)
    SUPERMASTER_ROLES = [SUPERMASTER]
    
    # All master roles
    MASTER_ROLES = [MASTER]
    
    # All roles
    ALL_ROLES = [SUPERMASTER, MASTER, AFFILIATE, TRADER, GUEST]
    
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
    def is_affiliate(role):
        """Check if role is affiliate level"""
        return role == Roles.AFFILIATE
    
    @staticmethod
    def normalize_role(role):
        """Normalize role to new naming convention"""
        role_mapping = {
            'agent': 'affiliate',  # Map old agent role to affiliate
            'super_admin': 'supermaster',
            'admin': 'master',
        }
        return role_mapping.get(role, role)
    
    @staticmethod
    def get_display_name(role):
        """Get display name for role"""
        display_names = {
            'supermaster': 'Super Master',
            'master': 'Master',
            'affiliate': 'Affiliate',
            'trader': 'Trader',
            'guest': 'Guest',
        }
        return display_names.get(role, role.title())


# Role hierarchy for user creation permissions
# FIXED: Proper hierarchy as per requirements
ROLE_HIERARCHY = {
    # Child SuperMaster can create: Master, Affiliate, Trader
    # Root SuperMaster can create SuperMaster (via can_create_same_role flag)
    'supermaster': ['master', 'affiliate', 'trader'],
    
    # Master can create: Affiliate, Trader only
    'master': ['affiliate', 'trader'],
    
    # Affiliate cannot create anyone (only gets referral code)
    'affiliate': [],
    
    # Trader cannot create anyone
    'trader': [],
    
    # Guest cannot create anyone
    'guest': []
}


def can_user_create_role(user_role, target_role, is_root_supermaster=False):
    """
    Check if a user with user_role can create a user with target_role
    
    Args:
        user_role: The role of the user trying to create
        target_role: The role being created
        is_root_supermaster: True if the user is the root SuperMaster (can_create_same_role=True)
    
    Returns:
        bool: True if allowed, False otherwise
    """
    # Root SuperMaster can create another SuperMaster
    if is_root_supermaster and user_role == Roles.SUPERMASTER and target_role == Roles.SUPERMASTER:
        return True
    
    # Check normal hierarchy
    allowed_roles = ROLE_HIERARCHY.get(user_role, [])
    return target_role in allowed_roles


# Hierarchy rules documentation
HIERARCHY_RULES = """
MarketEdgePros Hierarchy System Rules:

1. SuperMaster (Root):
   - Identified by: can_create_same_role = True
   - Can create: SuperMaster, Master, Affiliate, Trader
   - Has: Full system access
   - Dashboard: Admin Dashboard with all features

2. SuperMaster (Child):
   - Identified by: role = 'supermaster' AND can_create_same_role = False
   - Can create: Master, Affiliate, Trader (NOT SuperMaster)
   - Has: Access to all users below them in hierarchy
   - Dashboard: Admin Dashboard (limited)

3. Master:
   - Can create: Affiliate, Trader only
   - Has: Access to Affiliates and Traders below them
   - Dashboard: Master Dashboard

4. Affiliate:
   - Can create: Nobody (uses referral code instead)
   - Has: Unique referral code for marketing
   - Sees: Only Traders who registered via their referral code
   - Dashboard: Affiliate Dashboard (stats, commissions, payouts)

5. Trader:
   - End user
   - Cannot create anyone
   - Dashboard: Trader Dashboard (challenges, payouts, trading)

Registration Rules:
- User registers via website → goes under Root SuperMaster
- User registers via Affiliate referral code → goes under that Affiliate
- Each user can only see/manage users in their downline
- No "jumping" levels in hierarchy
"""

