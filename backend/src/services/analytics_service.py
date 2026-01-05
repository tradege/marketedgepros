"""
Analytics Service
Provides advanced analytics and reporting functionality
"""
from datetime import datetime, timedelta
from sqlalchemy import func, and_, extract, case
from src.database import db
from src.models.user import User
from src.models.trading_program import Challenge
from src.models.payment import Payment
from src.models.commission import Commission
from src.models.referral import Referral
from src.models.agent import Agent
import logging

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service for analytics and reporting"""
    
    @staticmethod
    def get_revenue_over_time(days=30):
        """
        Get revenue data over time
        
        Args:
            days: Number of days to look back
            
        Returns:
            List of daily revenue data
        """
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Query daily revenue
            daily_revenue = db.session.query(
                func.date(Payment.created_at).label('date'),
                func.sum(Payment.amount).label('revenue'),
                func.count(Payment.id).label('transactions')
            ).filter(
                and_(
                    Payment.status == 'completed',
                    Payment.created_at >= start_date
                )
            ).group_by(
                func.date(Payment.created_at)
            ).order_by(
                func.date(Payment.created_at)
            ).all()
            
            return [{
                'date': str(row.date),
                'revenue': float(row.revenue),
                'transactions': row.transactions
            } for row in daily_revenue]
            
        except Exception as e:
            logger.error(f'Error getting revenue over time: {str(e)}')
            return []
    
    @staticmethod
    def get_user_growth(days=30):
        """
        Get user registration growth over time
        
        Args:
            days: Number of days to look back
            
        Returns:
            List of daily user registration data
        """
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Query daily registrations
            daily_users = db.session.query(
                func.date(User.created_at).label('date'),
                func.count(User.id).label('registrations'),
                func.sum(case((User.is_active == True, 1), else_=0)).label('active')
            ).filter(
                User.created_at >= start_date
            ).group_by(
                func.date(User.created_at)
            ).order_by(
                func.date(User.created_at)
            ).all()
            
            # Calculate cumulative total
            cumulative = 0
            result = []
            for row in daily_users:
                cumulative += row.registrations
                result.append({
                    'date': str(row.date),
                    'registrations': row.registrations,
                    'active': row.active,
                    'cumulative': cumulative
                })
            
            return result
            
        except Exception as e:
            logger.error(f'Error getting user growth: {str(e)}')
            return []
    
    @staticmethod
    def get_challenge_statistics(days=30):
        """
        Get challenge statistics over time
        
        Args:
            days: Number of days to look back
            
        Returns:
            Challenge statistics data
        """
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Query challenge status distribution
            status_distribution = db.session.query(
                Challenge.status,
                func.count(Challenge.id).label('count')
            ).filter(
                Challenge.created_at >= start_date
            ).group_by(
                Challenge.status
            ).all()
            
            # Query daily challenge creation
            daily_challenges = db.session.query(
                func.date(Challenge.created_at).label('date'),
                func.count(Challenge.id).label('created'),
                func.sum(case((Challenge.status == 'completed', 1), else_=0)).label('completed'),
                func.sum(case((Challenge.status == 'funded', 1), else_=0)).label('funded')
            ).filter(
                Challenge.created_at >= start_date
            ).group_by(
                func.date(Challenge.created_at)
            ).order_by(
                func.date(Challenge.created_at)
            ).all()
            
            return {
                'status_distribution': [{
                    'status': row.status,
                    'count': row.count
                } for row in status_distribution],
                'daily_data': [{
                    'date': str(row.date),
                    'created': row.created,
                    'completed': row.completed,
                    'funded': row.funded
                } for row in daily_challenges]
            }
            
        except Exception as e:
            logger.error(f'Error getting challenge statistics: {str(e)}')
            return {'status_distribution': [], 'daily_data': []}
    
    @staticmethod
    def get_kyc_statistics():
        """
        Get KYC verification statistics
        
        Returns:
            KYC statistics data
        """
        try:
            # Query KYC status distribution
            kyc_distribution = db.session.query(
                User.kyc_status,
                func.count(User.id).label('count')
            ).group_by(
                User.kyc_status
            ).all()
            
            # Query recent KYC submissions (last 30 days)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_kyc = db.session.query(
                func.date(User.kyc_submitted_at).label('date'),
                func.count(User.id).label('submissions')
            ).filter(
                and_(
                    User.kyc_submitted_at.isnot(None),
                    User.kyc_submitted_at >= thirty_days_ago
                )
            ).group_by(
                func.date(User.kyc_submitted_at)
            ).order_by(
                func.date(User.kyc_submitted_at)
            ).all()
            
            return {
                'distribution': [{
                    'status': row.kyc_status or 'not_submitted',
                    'count': row.count
                } for row in kyc_distribution],
                'recent_submissions': [{
                    'date': str(row.date),
                    'submissions': row.submissions
                } for row in recent_kyc]
            }
            
        except Exception as e:
            logger.error(f'Error getting KYC statistics: {str(e)}')
            return {'distribution': [], 'recent_submissions': []}
    
    @staticmethod
    def get_referral_statistics():
        """
        Get referral and MLM statistics
        
        Returns:
            Referral statistics data
        """
        try:
            # Top performing agents
            top_agents = db.session.query(
                Agent.id,
                Agent.user_id,
                func.count(Referral.id).label('referral_count'),
                func.sum(Commission.commission_amount).label('total_commission')
            ).outerjoin(
                Referral, Referral.agent_id == Agent.id
            ).outerjoin(
                Commission, Commission.agent_id == Agent.id
            ).group_by(
                Agent.id, Agent.user_id
            ).order_by(
                func.count(Referral.id).desc()
            ).limit(10).all()
            
            # Get agent user details
            top_agents_data = []
            for row in top_agents:
                user = User.query.get(row.user_id)
                if user:
                    top_agents_data.append({
                        'agent_id': row.id,
                        'name': f"{user.first_name} {user.last_name}",
                        'email': user.email,
                        'referrals': row.referral_count,
                        'total_commission': float(row.total_commission or 0)
                    })
            
            # Referral conversion rate
            total_referrals = Referral.query.count()
            active_referrals = Referral.query.filter_by(status='active').count()
            conversion_rate = (active_referrals / total_referrals * 100) if total_referrals > 0 else 0
            
            return {
                'top_agents': top_agents_data,
                'total_referrals': total_referrals,
                'active_referrals': active_referrals,
                'conversion_rate': round(conversion_rate, 2)
            }
            
        except Exception as e:
            logger.error(f'Error getting referral statistics: {str(e)}')
            return {
                'top_agents': [],
                'total_referrals': 0,
                'active_referrals': 0,
                'conversion_rate': 0
            }
    
    @staticmethod
    def get_payment_statistics(days=30):
        """
        Get payment method and status statistics
        
        Args:
            days: Number of days to look back
            
        Returns:
            Payment statistics data
        """
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Payment method distribution
            method_distribution = db.session.query(
                Payment.payment_method,
                func.count(Payment.id).label('count'),
                func.sum(Payment.amount).label('total_amount')
            ).filter(
                and_(
                    Payment.created_at >= start_date,
                    Payment.status == 'completed'
                )
            ).group_by(
                Payment.payment_method
            ).all()
            
            # Payment status distribution
            status_distribution = db.session.query(
                Payment.status,
                func.count(Payment.id).label('count')
            ).filter(
                Payment.created_at >= start_date
            ).group_by(
                Payment.status
            ).all()
            
            return {
                'method_distribution': [{
                    'method': row.payment_method or 'unknown',
                    'count': row.count,
                    'total_amount': float(row.total_amount)
                } for row in method_distribution],
                'status_distribution': [{
                    'status': row.status,
                    'count': row.count
                } for row in status_distribution]
            }
            
        except Exception as e:
            logger.error(f'Error getting payment statistics: {str(e)}')
            return {'method_distribution': [], 'status_distribution': []}
    
    @staticmethod
    def get_comprehensive_analytics(days=30):
        """
        Get comprehensive analytics data for dashboard
        
        Args:
            days: Number of days to look back
            
        Returns:
            Comprehensive analytics data
        """
        try:
            return {
                'revenue_over_time': AnalyticsService.get_revenue_over_time(days),
                'user_growth': AnalyticsService.get_user_growth(days),
                'challenge_statistics': AnalyticsService.get_challenge_statistics(days),
                'kyc_statistics': AnalyticsService.get_kyc_statistics(),
                'referral_statistics': AnalyticsService.get_referral_statistics(),
                'payment_statistics': AnalyticsService.get_payment_statistics(days)
            }
        except Exception as e:
            logger.error(f'Error getting comprehensive analytics: {str(e)}')
            return {}

