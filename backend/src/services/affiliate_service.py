"""
Affiliate Service
Handles affiliate tracking, commission calculation, and conversions
"""
from datetime import datetime, timedelta
from decimal import Decimal
from flask import request
from sqlalchemy import func

from src.database import db
from src.models.affiliate import (
    AffiliateLink, AffiliateReferral, AffiliateCommission, AffiliateSettings
)
from src.models.user import User


class AffiliateService:
    """Service for affiliate tracking and management"""
    
    @staticmethod
    def track_click(ref_code, landing_page=None):
        """
        Track affiliate link click
        Returns affiliate_link_id if valid, None otherwise
        """
        try:
            # Find affiliate link
            affiliate_link = AffiliateLink.query.filter_by(
                code=ref_code,
                is_active=True
            ).first()
            
            if not affiliate_link:
                return None
            
            # Update click count
            affiliate_link.clicks += 1
            affiliate_link.last_click_at = datetime.utcnow()
            
            # Get request info
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent', '')[:500]
            
            # Create referral record
            referral = AffiliateReferral(
                affiliate_link_id=affiliate_link.id,
                affiliate_user_id=affiliate_link.user_id,
                ip_address=ip_address,
                user_agent=user_agent,
                landing_page=landing_page or request.referrer or '/'
            )
            
            db.session.add(referral)
            db.session.commit()
            
            return affiliate_link.id
            
        except Exception as e:
            db.session.rollback()
            print(f'Track click error: {str(e)}')
            return None
    
    @staticmethod
    def track_conversion(user_id, program_id, purchase_amount, ref_code=None):
        """
        Track affiliate conversion
        Creates commission if referral exists
        """
        try:
            # Find referral
            referral = None
            
            if ref_code:
                # Find by ref code
                affiliate_link = AffiliateLink.query.filter_by(code=ref_code).first()
                if affiliate_link:
                    referral = AffiliateReferral.query.filter_by(
                        affiliate_link_id=affiliate_link.id,
                        referred_user_id=None
                    ).order_by(AffiliateReferral.click_date.desc()).first()
            else:
                # Find recent referral for this user
                settings = AffiliateSettings.query.first()
                cookie_duration = settings.cookie_duration_days if settings else 30
                
                cutoff_date = datetime.utcnow() - timedelta(days=cookie_duration)
                
                referral = AffiliateReferral.query.filter(
                    AffiliateReferral.ip_address == request.remote_addr,
                    AffiliateReferral.referred_user_id == None,
                    AffiliateReferral.click_date >= cutoff_date
                ).order_by(AffiliateReferral.click_date.desc()).first()
            
            if not referral:
                return None
            
            # Update referral
            referral.referred_user_id = user_id
            referral.status = 'converted'
            referral.program_id = program_id
            referral.purchase_amount = purchase_amount
            referral.conversion_date = datetime.utcnow()
            
            # Calculate commission
            affiliate_link = AffiliateLink.query.get(referral.affiliate_link_id)
            
            # Safe commission calculation with zero check
            if affiliate_link.commission_rate and affiliate_link.commission_rate > 0:
                commission_amount = Decimal(str(purchase_amount)) * (Decimal(str(affiliate_link.commission_rate)) / Decimal('100'))
            else:
                commission_amount = Decimal('0')
            
            referral.commission_amount = commission_amount
            
            # Update affiliate link stats
            affiliate_link.conversions += 1
            affiliate_link.total_revenue += purchase_amount
            affiliate_link.total_commission += commission_amount
            
            # Create commission record
            commission = AffiliateCommission(
                affiliate_user_id=referral.affiliate_user_id,
                referral_id=referral.id,
                amount=commission_amount,
                type='one_time',
                status='pending',
                description=f'Commission from program #{program_id} purchase'
            )
            
            db.session.add(commission)
            
            # Auto-approve if enabled
            settings = AffiliateSettings.query.first()
            if settings and settings.auto_approve_commissions:
                commission.status = 'approved'
                commission.approved_at = datetime.utcnow()
            
            db.session.commit()
            
            return commission.id
            
        except Exception as e:
            db.session.rollback()
            print(f'Track conversion error: {str(e)}')
            return None
    
    @staticmethod
    def get_affiliate_stats(user_id):
        """Get comprehensive affiliate statistics - OPTIMIZED"""
        try:
            # Single query with aggregation - much faster!
            stats_query = db.session.query(
                func.coalesce(func.sum(AffiliateLink.clicks), 0).label('total_clicks'),
                func.coalesce(func.sum(AffiliateLink.conversions), 0).label('total_conversions'),
                func.coalesce(func.sum(AffiliateLink.total_revenue), 0).label('total_revenue'),
                func.coalesce(func.sum(AffiliateLink.total_commission), 0).label('total_commission')
            ).filter(
                AffiliateLink.user_id == user_id
            ).first()
            
            if not stats_query or stats_query.total_clicks == 0:
                return None
            
            # Get commission breakdown with single query
            commission_stats = db.session.query(
                AffiliateCommission.status,
                func.coalesce(func.sum(AffiliateCommission.amount), 0).label('total')
            ).filter(
                AffiliateCommission.affiliate_user_id == user_id
            ).group_by(AffiliateCommission.status).all()
            
            # Convert to dict
            commission_breakdown = {status: float(total) for status, total in commission_stats}
            
            # Get monthly stats (last 12 months)
            monthly_stats = db.session.query(
                func.date_trunc('month', AffiliateReferral.conversion_date).label('month'),
                func.count(AffiliateReferral.id).label('conversions'),
                func.coalesce(func.sum(AffiliateReferral.commission_amount), 0).label('commission')
            ).filter(
                AffiliateReferral.affiliate_user_id == user_id,
                AffiliateReferral.status == 'converted',
                AffiliateReferral.conversion_date >= datetime.utcnow() - timedelta(days=365)
            ).group_by('month').order_by('month').all()
            
            return {
                'total_clicks': int(stats_query.total_clicks),
                'total_conversions': int(stats_query.total_conversions),
                'total_revenue': float(stats_query.total_revenue),
                'total_commission': float(stats_query.total_commission),
                'conversion_rate': round(
                    (stats_query.total_conversions / stats_query.total_clicks * 100) 
                    if stats_query.total_clicks > 0 else 0, 
                    2
                ),
                'commissions': {
                    'pending': commission_breakdown.get('pending', 0.0),
                    'approved': commission_breakdown.get('approved', 0.0),
                    'paid': commission_breakdown.get('paid', 0.0),
                    'available_for_payout': commission_breakdown.get('approved', 0.0)
                },
                'monthly_stats': [
                    {
                        'month': stat.month.strftime('%Y-%m') if stat.month else None,
                        'conversions': int(stat.conversions),
                        'commission': float(stat.commission)
                    }
                    for stat in monthly_stats
                ]
            }
            
        except Exception as e:
            print(f'Get affiliate stats error: {str(e)}')
            return None
    @staticmethod
    def calculate_commission(purchase_amount, commission_rate):
        """
        Calculate commission amount with safe division
        
        Args:
            purchase_amount: Purchase amount (Decimal, float, or int)
            commission_rate: Commission rate percentage (Decimal, float, or int)
        
        Returns:
            Decimal: Calculated commission amount
        """
        if not purchase_amount or not commission_rate:
            return Decimal('0')
        
        if commission_rate <= 0:
            return Decimal('0')
        
        # Convert to Decimal for precise calculations
        amount_decimal = Decimal(str(purchase_amount))
        rate_decimal = Decimal(str(commission_rate))
        
        # Calculate with safe division
        commission = (amount_decimal * rate_decimal) / Decimal('100')
        
        return commission.quantize(Decimal('0.01'))
    
    @staticmethod
    def get_top_affiliates(limit=10):
        """Get top performing affiliates"""
        try:
            top_affiliates = db.session.query(
                User.id,
                User.email,
                User.first_name,
                User.last_name,
                func.sum(AffiliateLink.total_revenue).label('total_revenue'),
                func.sum(AffiliateLink.total_commission).label('total_commission'),
                func.sum(AffiliateLink.conversions).label('total_conversions')
            ).join(
                AffiliateLink, User.id == AffiliateLink.user_id
            ).group_by(
                User.id, User.email, User.first_name, User.last_name
            ).order_by(
                func.sum(AffiliateLink.total_revenue).desc()
            ).limit(limit).all()
            
            return [
                {
                    'user_id': aff.id,
                    'email': aff.email,
                    'name': f'{aff.first_name} {aff.last_name}',
                    'total_revenue': float(aff.total_revenue) if aff.total_revenue else 0,
                    'total_commission': float(aff.total_commission) if aff.total_commission else 0,
                    'total_conversions': aff.total_conversions or 0
                }
                for aff in top_affiliates
            ]
            
        except Exception as e:
            print(f'Get top affiliates error: {str(e)}')
            return []
    
    @staticmethod
    def validate_payout_request(user_id):
        """Validate if user can request payout"""
        try:
            # Get approved commissions
            approved_commissions = AffiliateCommission.query.filter_by(
                affiliate_user_id=user_id,
                status='approved',
                payout_id=None
            ).all()
            
            if not approved_commissions:
                return False, 'No approved commissions available'
            
            total_amount = sum(c.amount for c in approved_commissions)
            
            # Check minimum payout
            settings = AffiliateSettings.query.first()
            if settings and total_amount < settings.min_payout_amount:
                return False, f'Minimum payout amount is ${float(settings.min_payout_amount)}'
            
            return True, total_amount
            
        except Exception as e:
            print(f'Validate payout error: {str(e)}')
            return False, 'Failed to validate payout request'

