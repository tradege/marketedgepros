"""
Affiliate Service
Handles affiliate tracking, commission calculation, and conversions
"""
from datetime import datetime, timedelta
from flask import request
from sqlalchemy import func

from src.extensions import db
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
            commission_amount = purchase_amount * (affiliate_link.commission_rate / 100)
            
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
        """Get comprehensive affiliate statistics"""
        try:
            # Get all links
            links = AffiliateLink.query.filter_by(user_id=user_id).all()
            
            if not links:
                return None
            
            # Calculate totals
            total_clicks = sum(link.clicks for link in links)
            total_conversions = sum(link.conversions for link in links)
            total_revenue = sum(link.total_revenue for link in links)
            total_commission = sum(link.total_commission for link in links)
            
            # Get commission breakdown
            commissions = AffiliateCommission.query.filter_by(affiliate_user_id=user_id).all()
            
            pending = sum(c.amount for c in commissions if c.status == 'pending')
            approved = sum(c.amount for c in commissions if c.status == 'approved')
            paid = sum(c.amount for c in commissions if c.status == 'paid')
            
            # Get monthly stats (last 12 months)
            monthly_stats = db.session.query(
                func.date_trunc('month', AffiliateReferral.conversion_date).label('month'),
                func.count(AffiliateReferral.id).label('conversions'),
                func.sum(AffiliateReferral.commission_amount).label('commission')
            ).filter(
                AffiliateReferral.affiliate_user_id == user_id,
                AffiliateReferral.status == 'converted',
                AffiliateReferral.conversion_date >= datetime.utcnow() - timedelta(days=365)
            ).group_by('month').order_by('month').all()
            
            return {
                'total_clicks': total_clicks,
                'total_conversions': total_conversions,
                'total_revenue': float(total_revenue),
                'total_commission': float(total_commission),
                'conversion_rate': round((total_conversions / total_clicks * 100) if total_clicks > 0 else 0, 2),
                'commissions': {
                    'pending': float(pending),
                    'approved': float(approved),
                    'paid': float(paid),
                    'available_for_payout': float(approved)
                },
                'monthly_stats': [
                    {
                        'month': stat.month.strftime('%Y-%m') if stat.month else None,
                        'conversions': stat.conversions,
                        'commission': float(stat.commission) if stat.commission else 0
                    }
                    for stat in monthly_stats
                ]
            }
            
        except Exception as e:
            print(f'Get affiliate stats error: {str(e)}')
            return None
    
    @staticmethod
    def calculate_commission(purchase_amount, commission_rate):
        """Calculate commission amount"""
        return purchase_amount * (commission_rate / 100)
    
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

