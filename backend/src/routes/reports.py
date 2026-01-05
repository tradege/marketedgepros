"""
Reports routes for analytics and commission tracking
"""
from flask import Blueprint, request, jsonify, g
from src.database import db
from src.models.user import User
from src.models.trading_program import Challenge
from src.models.trade import Trade
from src.models.payment import Payment
from src.models.commission import Commission
from src.models.referral import Referral
from src.models.agent import Agent
from src.utils.decorators import token_required, admin_required
from datetime import datetime, timedelta
from sqlalchemy import func, and_, desc, extract
from collections import defaultdict

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/agent/dashboard', methods=['GET'])
@token_required
def get_agent_dashboard():
    """Get agent dashboard statistics"""
    try:
        user_id = g.current_user.id
        
        # Check if user is an agent
        agent = Agent.query.filter_by(user_id=user_id).first()
        if not agent:
            return jsonify({'error': 'User is not an agent'}), 403
        
        # Get all referrals
        referrals = Referral.query.filter_by(agent_id=agent.id).all()
        trader_ids = [r.referred_user_id for r in referrals]
        
        # Trader statistics
        total_traders = len(trader_ids)
        active_traders = User.query.filter(
            and_(
                User.id.in_(trader_ids),
                User.is_active == True
            )
        ).count()
        
        # Get funded traders (traders with funded challenges)
        funded_traders = db.session.query(Challenge.user_id).filter(
            and_(
                Challenge.user_id.in_(trader_ids),
                Challenge.status == 'funded'
            )
        ).distinct().count()
        
        # Commission statistics
        total_commissions = db.session.query(func.sum(Commission.amount)).filter(
            Commission.agent_id == agent.id
        ).scalar() or 0
        
        pending_commissions = db.session.query(func.sum(Commission.amount)).filter(
            and_(
                Commission.agent_id == agent.id,
                Commission.status == 'pending'
            )
        ).scalar() or 0
        
        # This month commissions
        first_day_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
        monthly_commissions = db.session.query(func.sum(Commission.amount)).filter(
            and_(
                Commission.agent_id == agent.id,
                Commission.created_at >= first_day_of_month
            )
        ).scalar() or 0
        
        # Challenge statistics for referred traders
        total_challenges = Challenge.query.filter(
            Challenge.user_id.in_(trader_ids)
        ).count()
        
        completed_challenges = Challenge.query.filter(
            and_(
                Challenge.user_id.in_(trader_ids),
                Challenge.status.in_(['completed', 'funded'])
            )
        ).count()
        
        pass_rate = (completed_challenges / total_challenges * 100) if total_challenges > 0 else 0
        
        # Average profit per trader
        total_profit = db.session.query(func.sum(Challenge.current_balance - Challenge.initial_balance)).filter(
            and_(
                Challenge.user_id.in_(trader_ids),
                Challenge.status == 'funded'
            )
        ).scalar() or 0
        
        avg_profit = (total_profit / funded_traders) if funded_traders > 0 else 0
        
        # Recent traders (last 5)
        recent_traders = User.query.filter(
            User.id.in_(trader_ids)
        ).order_by(desc(User.created_at)).limit(5).all()
        
        # Recent commissions (last 5)
        recent_commissions = Commission.query.filter_by(
            agent_id=agent.id
        ).order_by(desc(Commission.created_at)).limit(5).all()
        
        return jsonify({
            'traders': {
                'total': total_traders,
                'active': active_traders,
                'funded': funded_traders
            },
            'commissions': {
                'total': float(total_commissions),
                'pending': float(pending_commissions),
                'this_month': float(monthly_commissions)
            },
            'performance': {
                'pass_rate': round(pass_rate, 2),
                'average_profit': round(float(avg_profit), 2),
                'total_challenges': total_challenges,
                'completed_challenges': completed_challenges
            },
            'recent_traders': [{
                'id': trader.id,
                'name': f"{trader.first_name} {trader.last_name}",
                'email': trader.email,
                'is_active': trader.is_active,
                'created_at': trader.created_at.isoformat()
            } for trader in recent_traders],
            'recent_commissions': [{
                'id': commission.id,
                'amount': float(commission.amount),
                'type': commission.commission_type,
                'status': commission.status,
                'created_at': commission.created_at.isoformat()
            } for commission in recent_commissions]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@reports_bp.route('/agent/traders', methods=['GET'])
@token_required
def get_agent_traders():
    """Get detailed list of agent's traders"""
    try:
        user_id = g.current_user.id
        
        # Check if user is an agent
        agent = Agent.query.filter_by(user_id=user_id).first()
        if not agent:
            return jsonify({'error': 'User is not an agent'}), 403
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        
        # Get referrals
        referrals = Referral.query.filter_by(agent_id=agent.id).all()
        trader_ids = [r.referred_user_id for r in referrals]
        
        # Build query
        query = User.query.filter(User.id.in_(trader_ids))
        
        if status:
            if status == 'funded':
                # Get users with funded challenges
                funded_user_ids = db.session.query(Challenge.user_id).filter(
                    and_(
                        Challenge.user_id.in_(trader_ids),
                        Challenge.status == 'funded'
                    )
                ).distinct().all()
                funded_ids = [uid[0] for uid in funded_user_ids]
                query = query.filter(User.id.in_(funded_ids))
            else:
                query = query.filter_by(status=status)
        
        # Paginate
        pagination = query.order_by(desc(User.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Get trader details with challenge info
        traders_data = []
        for trader in pagination.items:
            # Get active challenge
            active_challenge = Challenge.query.filter_by(
                user_id=trader.id,
                status='active'
            ).first()
            
            # Get all challenges
            all_challenges = Challenge.query.filter_by(user_id=trader.id).all()
            
            # Calculate win rate
            completed = [c for c in all_challenges if c.status in ['completed', 'funded']]
            failed = [c for c in all_challenges if c.status == 'failed']
            win_rate = (len(completed) / len(all_challenges) * 100) if all_challenges else 0
            
            trader_info = {
                'id': trader.id,
                'name': f"{trader.first_name} {trader.last_name}",
                'email': trader.email,
                'is_active': trader.is_active,
                'created_at': trader.created_at.isoformat(),
                'challenge': None,
                'win_rate': round(win_rate, 2)
            }
            
            if active_challenge:
                balance = float(active_challenge.current_balance)
                initial = float(active_challenge.initial_balance)
                pnl = balance - initial
                pnl_percentage = (pnl / initial * 100) if initial > 0 else 0
                
                trader_info['challenge'] = {
                    'phase': active_challenge.phase,
                    'balance': balance,
                    'profit_loss': pnl,
                    'profit_loss_percentage': round(pnl_percentage, 2),
                    'status': active_challenge.status
                }
            
            traders_data.append(trader_info)
        
        return jsonify({
            'traders': traders_data,
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@reports_bp.route('/agent/commissions', methods=['GET'])
@token_required
def get_agent_commissions():
    """Get agent commission history"""
    try:
        user_id = g.current_user.id
        
        # Check if user is an agent
        agent = Agent.query.filter_by(user_id=user_id).first()
        if not agent:
            return jsonify({'error': 'User is not an agent'}), 403
        
        # Get query parameters
        period = request.args.get('period', 'all')
        
        # Build query
        query = Commission.query.filter_by(agent_id=agent.id)
        
        # Apply period filter
        if period == 'month':
            first_day = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
            query = query.filter(Commission.created_at >= first_day)
        elif period == 'last_month':
            # Get first day of last month
            first_day_this_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
            last_month = first_day_this_month - timedelta(days=1)
            first_day_last_month = last_month.replace(day=1, hour=0, minute=0, second=0)
            query = query.filter(
                and_(
                    Commission.created_at >= first_day_last_month,
                    Commission.created_at < first_day_this_month
                )
            )
        elif period == 'year':
            first_day_year = datetime.utcnow().replace(month=1, day=1, hour=0, minute=0, second=0)
            query = query.filter(Commission.created_at >= first_day_year)
        
        # Get commissions
        commissions = query.order_by(desc(Commission.created_at)).all()
        
        # Calculate statistics
        total_earned = sum([float(c.amount) for c in commissions if c.status == 'paid'])
        pending = sum([float(c.amount) for c in commissions if c.status == 'pending'])
        this_month_earned = sum([
            float(c.amount) for c in commissions 
            if c.status == 'paid' and c.created_at.month == datetime.utcnow().month
        ])
        
        return jsonify({
            'statistics': {
                'total_earned': round(total_earned, 2),
                'this_month': round(this_month_earned, 2),
                'pending': round(pending, 2),
                'paid_out': round(total_earned, 2)
            },
            'commission_types': {
                'enrollment': {'rate': 0.30, 'description': '30% of program price'},
                'profit_share': {'rate': 0.10, 'description': '10% of trader profits'},
                'renewal': {'rate': 0.20, 'description': '20% of renewal fees'}
            },
            'commissions': [{
                'id': commission.id,
                'trader_id': commission.trader_id,
                'trader_name': f"{User.query.get(commission.trader_id).first_name} {User.query.get(commission.trader_id).last_name}" if commission.trader_id else 'N/A',
                'type': commission.commission_type,
                'program': commission.program_name if hasattr(commission, 'program_name') else 'N/A',
                'rate': float(commission.commission_rate) if commission.commission_rate else 0,
                'amount': float(commission.amount),
                'status': commission.status,
                'created_at': commission.created_at.isoformat(),
                'paid_at': commission.paid_at.isoformat() if commission.paid_at else None
            } for commission in commissions]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@reports_bp.route('/agent/analytics', methods=['GET'])
@token_required
def get_agent_analytics():
    """Get agent performance analytics"""
    try:
        user_id = g.current_user.id
        
        # Check if user is an agent
        agent = Agent.query.filter_by(user_id=user_id).first()
        if not agent:
            return jsonify({'error': 'User is not an agent'}), 403
        
        # Get referrals
        referrals = Referral.query.filter_by(agent_id=agent.id).all()
        trader_ids = [r.referred_user_id for r in referrals]
        
        # Monthly trends (last 12 months)
        monthly_data = defaultdict(lambda: {'traders': 0, 'commissions': 0, 'funded': 0})
        
        # Get new traders per month
        for i in range(12):
            month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0) - timedelta(days=30*i)
            month_end = month_start + timedelta(days=30)
            
            new_traders = User.query.filter(
                and_(
                    User.id.in_(trader_ids),
                    User.created_at >= month_start,
                    User.created_at < month_end
                )
            ).count()
            
            month_commissions = db.session.query(func.sum(Commission.amount)).filter(
                and_(
                    Commission.agent_id == agent.id,
                    Commission.created_at >= month_start,
                    Commission.created_at < month_end
                )
            ).scalar() or 0
            
            funded_count = db.session.query(Challenge.user_id).filter(
                and_(
                    Challenge.user_id.in_(trader_ids),
                    Challenge.status == 'funded',
                    Challenge.funded_at >= month_start,
                    Challenge.funded_at < month_end
                )
            ).distinct().count()
            
            month_key = month_start.strftime('%Y-%m')
            monthly_data[month_key] = {
                'traders': new_traders,
                'commissions': float(month_commissions),
                'funded': funded_count
            }
        
        # Top performing traders
        top_traders = []
        for trader_id in trader_ids[:10]:  # Limit to top 10
            trader = User.query.get(trader_id)
            if not trader:
                continue
            
            # Get funded challenges
            funded_challenges = Challenge.query.filter_by(
                user_id=trader_id,
                status='funded'
            ).all()
            
            if not funded_challenges:
                continue
            
            # Calculate total profit
            total_profit = sum([
                float(c.current_balance - c.initial_balance)
                for c in funded_challenges
            ])
            
            # Get trades
            challenge_ids = [c.id for c in funded_challenges]
            trades = Trade.query.filter(Trade.challenge_id.in_(challenge_ids)).all()
            
            winning_trades = len([t for t in trades if t.profit > 0])
            total_trades = len(trades)
            win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
            
            top_traders.append({
                'trader_id': trader.id,
                'name': f"{trader.first_name} {trader.last_name}",
                'profit': round(total_profit, 2),
                'win_rate': round(win_rate, 2),
                'total_trades': total_trades
            })
        
        # Sort by profit
        top_traders.sort(key=lambda x: x['profit'], reverse=True)
        
        # Add rank
        for i, trader in enumerate(top_traders[:10], 1):
            trader['rank'] = i
        
        # Overall statistics
        total_traders = len(trader_ids)
        active_traders = User.query.filter(
            and_(User.id.in_(trader_ids), User.is_active == True)
        ).count()
        
        total_commissions = db.session.query(func.sum(Commission.amount)).filter(
            Commission.agent_id == agent.id
        ).scalar() or 0
        
        avg_commission_per_trader = (total_commissions / total_traders) if total_traders > 0 else 0
        
        # Performance metrics
        all_challenges = Challenge.query.filter(Challenge.user_id.in_(trader_ids)).all()
        completed = len([c for c in all_challenges if c.status in ['completed', 'funded']])
        total = len(all_challenges)
        pass_rate = (completed / total * 100) if total > 0 else 0
        
        # Calculate average win rate
        all_trades = Trade.query.filter(
            Trade.challenge_id.in_([c.id for c in all_challenges])
        ).all()
        winning = len([t for t in all_trades if t.profit > 0])
        total_trades_count = len(all_trades)
        avg_win_rate = (winning / total_trades_count * 100) if total_trades_count > 0 else 0
        
        # Average profit per trader
        funded_challenges = [c for c in all_challenges if c.status == 'funded']
        total_profit = sum([
            float(c.current_balance - c.initial_balance)
            for c in funded_challenges
        ])
        avg_profit = (total_profit / len(funded_challenges)) if funded_challenges else 0
        
        # Funded accounts
        funded_accounts = len(funded_challenges)
        
        return jsonify({
            'overview': {
                'new_traders': User.query.filter(
                    and_(
                        User.id.in_(trader_ids),
                        User.created_at >= datetime.utcnow() - timedelta(days=30)
                    )
                ).count(),
                'active_traders': active_traders,
                'total_commissions': round(float(total_commissions), 2),
                'avg_commission_per_trader': round(avg_commission_per_trader, 2)
            },
            'performance': {
                'pass_rate': round(pass_rate, 2),
                'avg_win_rate': round(avg_win_rate, 2),
                'avg_profit_per_trader': round(avg_profit, 2),
                'funded_accounts': funded_accounts
            },
            'monthly_trends': dict(sorted(monthly_data.items())),
            'top_traders': top_traders[:10]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@reports_bp.route('/admin/analytics', methods=['GET'])
@token_required
@admin_required
def get_admin_analytics():
    """Get comprehensive admin analytics"""
    try:
        # User growth
        total_users = User.query.count()
        new_users_month = User.query.filter(
            User.created_at >= datetime.utcnow() - timedelta(days=30)
        ).count()
        
        # Revenue
        total_revenue = db.session.query(func.sum(Payment.amount)).filter(
            Payment.status == 'completed'
        ).scalar() or 0
        
        monthly_revenue = db.session.query(func.sum(Payment.amount)).filter(
            and_(
                Payment.status == 'completed',
                Payment.created_at >= datetime.utcnow() - timedelta(days=30)
            )
        ).scalar() or 0
        
        # Challenges
        total_challenges = Challenge.query.count()
        active_challenges = Challenge.query.filter_by(status='active').count()
        funded_challenges = Challenge.query.filter_by(status='funded').count()
        
        # Success rate
        completed = Challenge.query.filter(
            Challenge.status.in_(['completed', 'funded'])
        ).count()
        success_rate = (completed / total_challenges * 100) if total_challenges > 0 else 0
        
        return jsonify({
            'users': {
                'total': total_users,
                'new_this_month': new_users_month,
                'growth_rate': round((new_users_month / total_users * 100), 2) if total_users > 0 else 0
            },
            'revenue': {
                'total': round(float(total_revenue), 2),
                'monthly': round(float(monthly_revenue), 2)
            },
            'challenges': {
                'total': total_challenges,
                'active': active_challenges,
                'funded': funded_challenges,
                'success_rate': round(success_rate, 2)
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

