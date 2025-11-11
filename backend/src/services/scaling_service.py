"""
Scaling Service
Handles account scaling logic - eligibility checks, upgrades, and progress tracking
"""
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy import and_, or_, func
from src.database import db
from src.models.account_scaling import AccountScaling, ScalingTier
from src.models.user import User
from src.models.trade import Trade
from src.models.trading_program import Challenge


class ScalingService:
    """Service for managing account scaling operations"""
    
    # Default scaling tiers (can be customized per tenant)
    DEFAULT_TIERS = [
        {'tier': 1, 'account_size': 10000, 'profit_target': 800, 'profit_split': 80},
        {'tier': 2, 'account_size': 25000, 'profit_target': 2000, 'profit_split': 80},
        {'tier': 3, 'account_size': 50000, 'profit_target': 4000, 'profit_split': 85},
        {'tier': 4, 'account_size': 100000, 'profit_target': 8000, 'profit_split': 90},
        {'tier': 5, 'account_size': 200000, 'profit_target': 16000, 'profit_split': 90},
    ]
    
    @staticmethod
    def initialize_scaling_for_user(user: User, starting_account_size: Decimal) -> AccountScaling:
        """
        Initialize scaling plan for a new funded trader
        """
        # Find which tier matches the starting account size
        tier_number = 1
        for i, tier in enumerate(ScalingService.DEFAULT_TIERS):
            if tier['account_size'] == float(starting_account_size):
                tier_number = i + 1
                break
        
        # Get tier configuration
        current_tier_config = ScalingService.DEFAULT_TIERS[tier_number - 1]
        next_tier_config = ScalingService.DEFAULT_TIERS[tier_number] if tier_number < len(ScalingService.DEFAULT_TIERS) else None
        
        # Create scaling record
        scaling = AccountScaling(
            user_id=user.id,
            current_tier=tier_number,
            current_account_size=starting_account_size,
            next_tier=tier_number + 1 if next_tier_config else None,
            next_account_size=Decimal(str(next_tier_config['account_size'])) if next_tier_config else None,
            total_profit=Decimal('0'),
            target_profit=Decimal(str(current_tier_config['profit_target'])),
            progress_percentage=Decimal('0'),
            status='active'
        )
        
        db.session.add(scaling)
        db.session.commit()
        
        return scaling
    
    @staticmethod
    def get_user_scaling(user_id: int) -> Optional[AccountScaling]:
        """Get scaling plan for a user"""
        return db.session.query(AccountScaling).filter(
            AccountScaling.user_id == user_id
        ).first()
    
    @staticmethod
    def update_profit(user_id: int, profit_amount: Decimal) -> Dict:
        """
        Update user's profit and check for scaling eligibility
        Called after a successful trade or payout
        """
        scaling = ScalingService.get_user_scaling(user_id)
        
        if not scaling:
            return {
                'success': False,
                'error': 'No scaling plan found for user'
            }
        
        if scaling.status != 'active':
            return {
                'success': False,
                'error': f'Scaling plan is {scaling.status}'
            }
        
        # Update profit
        old_progress = float(scaling.progress_percentage)
        scaling.update_progress(profit_amount)
        db.session.commit()
        
        return {
            'success': True,
            'total_profit': float(scaling.total_profit),
            'target_profit': float(scaling.target_profit),
            'progress_percentage': float(scaling.progress_percentage),
            'progress_increased': float(scaling.progress_percentage) - old_progress,
            'is_eligible': scaling.is_eligible_for_scaling,
            'next_tier': scaling.next_tier,
            'next_account_size': float(scaling.next_account_size) if scaling.next_account_size else None
        }
    
    @staticmethod
    def check_eligibility(user_id: int) -> Dict:
        """
        Check if user is eligible for scaling
        Returns detailed eligibility information
        """
        scaling = ScalingService.get_user_scaling(user_id)
        
        if not scaling:
            return {
                'eligible': False,
                'reason': 'No scaling plan found'
            }
        
        if scaling.status != 'active':
            return {
                'eligible': False,
                'reason': f'Scaling plan is {scaling.status}'
            }
        
        if not scaling.next_tier:
            return {
                'eligible': False,
                'reason': 'Already at maximum tier'
            }
        
        # Check profit target
        if scaling.progress_percentage < 100:
            return {
                'eligible': False,
                'reason': 'Profit target not met',
                'progress': float(scaling.progress_percentage),
                'remaining_profit': float(scaling.target_profit - scaling.total_profit)
            }
        
        # Check minimum trading days (if configured)
        # TODO: Implement trading days check
        
        # Check minimum trades (if configured)
        # TODO: Implement minimum trades check
        
        return {
            'eligible': True,
            'current_tier': scaling.current_tier,
            'current_account_size': float(scaling.current_account_size),
            'next_tier': scaling.next_tier,
            'next_account_size': float(scaling.next_account_size),
            'total_profit': float(scaling.total_profit)
        }
    
    @staticmethod
    def perform_scale_up(user_id: int) -> Dict:
        """
        Scale user up to next tier
        Creates new challenge with larger account size
        """
        scaling = ScalingService.get_user_scaling(user_id)
        
        if not scaling:
            return {
                'success': False,
                'error': 'No scaling plan found'
            }
        
        # Check eligibility
        eligibility = ScalingService.check_eligibility(user_id)
        if not eligibility.get('eligible'):
            return {
                'success': False,
                'error': eligibility.get('reason', 'Not eligible for scaling')
            }
        
        # Get next tier configuration
        next_tier_number = scaling.next_tier
        if next_tier_number > len(ScalingService.DEFAULT_TIERS):
            return {
                'success': False,
                'error': 'No next tier available'
            }
        
        next_tier_config = ScalingService.DEFAULT_TIERS[next_tier_number - 1]
        
        # Perform scale up
        new_account_size = Decimal(str(next_tier_config['account_size']))
        new_target_profit = Decimal(str(next_tier_config['profit_target']))
        
        # Update scaling record
        old_tier = scaling.current_tier
        old_account_size = float(scaling.current_account_size)
        
        # Determine next tier after this one
        tier_after_next = next_tier_number + 1 if next_tier_number < len(ScalingService.DEFAULT_TIERS) else None
        next_account_after = ScalingService.DEFAULT_TIERS[tier_after_next - 1]['account_size'] if tier_after_next else None
        
        scaling.current_tier = next_tier_number
        scaling.current_account_size = new_account_size
        scaling.next_tier = tier_after_next
        scaling.next_account_size = Decimal(str(next_account_after)) if next_account_after else None
        scaling.total_profit = Decimal('0')
        scaling.target_profit = new_target_profit
        scaling.progress_percentage = Decimal('0')
        scaling.times_scaled += 1
        scaling.last_scaled_at = datetime.utcnow()
        scaling.is_eligible_for_scaling = False
        
        # Check if reached max tier
        if not tier_after_next:
            scaling.status = 'completed'
        
        db.session.commit()
        
        return {
            'success': True,
            'message': f'Successfully scaled from tier {old_tier} to tier {next_tier_number}',
            'old_tier': old_tier,
            'old_account_size': old_account_size,
            'new_tier': next_tier_number,
            'new_account_size': float(new_account_size),
            'new_target_profit': float(new_target_profit),
            'times_scaled': scaling.times_scaled,
            'is_max_tier': scaling.status == 'completed'
        }
    
    @staticmethod
    def get_scaling_history(user_id: int) -> Dict:
        """Get user's scaling history and current status"""
        scaling = ScalingService.get_user_scaling(user_id)
        
        if not scaling:
            return {
                'has_scaling_plan': False
            }
        
        return {
            'has_scaling_plan': True,
            'current_tier': scaling.current_tier,
            'current_account_size': float(scaling.current_account_size),
            'next_tier': scaling.next_tier,
            'next_account_size': float(scaling.next_account_size) if scaling.next_account_size else None,
            'total_profit': float(scaling.total_profit),
            'target_profit': float(scaling.target_profit),
            'progress_percentage': float(scaling.progress_percentage),
            'times_scaled': scaling.times_scaled,
            'last_scaled_at': scaling.last_scaled_at.isoformat() if scaling.last_scaled_at else None,
            'is_eligible_for_scaling': scaling.is_eligible_for_scaling,
            'status': scaling.status,
            'created_at': scaling.created_at.isoformat() if scaling.created_at else None
        }
    
    @staticmethod
    def get_all_tiers() -> List[Dict]:
        """Get all available scaling tiers"""
        return [
            {
                'tier_number': tier['tier'],
                'account_size': tier['account_size'],
                'profit_target': tier['profit_target'],
                'profit_split': tier['profit_split']
            }
            for tier in ScalingService.DEFAULT_TIERS
        ]
    
    @staticmethod
    def pause_scaling(user_id: int) -> Dict:
        """Pause scaling plan for a user"""
        scaling = ScalingService.get_user_scaling(user_id)
        
        if not scaling:
            return {'success': False, 'error': 'No scaling plan found'}
        
        scaling.status = 'paused'
        db.session.commit()
        
        return {'success': True, 'message': 'Scaling plan paused'}
    
    @staticmethod
    def resume_scaling(user_id: int) -> Dict:
        """Resume scaling plan for a user"""
        scaling = ScalingService.get_user_scaling(user_id)
        
        if not scaling:
            return {'success': False, 'error': 'No scaling plan found'}
        
        if scaling.status == 'completed':
            return {'success': False, 'error': 'Cannot resume completed scaling plan'}
        
        scaling.status = 'active'
        db.session.commit()
        
        return {'success': True, 'message': 'Scaling plan resumed'}
