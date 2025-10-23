"""
Challenge routes for managing trading challenges
"""
from flask import Blueprint, request, jsonify, g
from src.database import db
from src.models.trading_program import Challenge
from src.models.trading_program import TradingProgram as Program
from src.models.trade import Trade
from src.models.payment import Payment
from src.utils.decorators import token_required, admin_required
from datetime import datetime
from sqlalchemy import desc, and_

challenges_bp = Blueprint('challenges', __name__)


@challenges_bp.route('/', methods=['POST'])
@token_required
def create_challenge():
    """Create a new challenge for the user"""
    try:
        user_id = g.current_user.id
        data = request.get_json()
        
        # Validate required fields
        if not data.get('program_id'):
            return jsonify({'error': 'Program ID is required'}), 400
        
        # Get program
        program = Program.query.get_or_404(data['program_id'])
        
        if not program.is_active:
            return jsonify({'error': 'Program is not active'}), 400
        
        # Check if user has already paid for this program
        # In a real implementation, verify payment first
        
        # Create challenge
        challenge = Challenge(
            user_id=user_id,
            program_id=program.id,
            status='pending',  # Will be 'active' after payment
            phase=1 if program.type == 'two_phase' else 0,
            initial_balance=program.account_size,
            current_balance=program.account_size,
            max_balance=program.account_size,
            profit_target=program.profit_target,
            max_daily_loss=program.max_daily_loss,
            max_total_drawdown=program.max_total_drawdown,
            min_trading_days=program.min_trading_days,
            trading_days=0
        )
        
        db.session.add(challenge)
        db.session.commit()
        
        return jsonify({
            'message': 'Challenge created successfully',
            'challenge': {
                'id': challenge.id,
                'program_id': challenge.program_id,
                'status': challenge.status,
                'phase': challenge.phase,
                'initial_balance': float(challenge.initial_balance),
                'created_at': challenge.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@challenges_bp.route('/<int:challenge_id>/start', methods=['POST'])
@token_required
def start_challenge(challenge_id):
    """Start a challenge (after payment confirmation)"""
    try:
        user_id = g.current_user.id
        
        challenge = Challenge.query.filter_by(
            id=challenge_id,
            user_id=user_id
        ).first_or_404()
        
        if challenge.status != 'pending':
            return jsonify({'error': 'Challenge cannot be started'}), 400
        
        # Update challenge status
        challenge.status = 'active'
        challenge.started_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Challenge started successfully',
            'challenge': {
                'id': challenge.id,
                'status': challenge.status,
                'started_at': challenge.started_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@challenges_bp.route('/<int:challenge_id>/evaluate', methods=['POST'])
@token_required
@admin_required
def evaluate_challenge(challenge_id):
    """Evaluate a challenge and update status"""
    try:
        challenge = Challenge.query.get_or_404(challenge_id)
        
        if challenge.status != 'active':
            return jsonify({'error': 'Challenge is not active'}), 400
        
        # Get all trades for this challenge
        trades = Trade.query.filter_by(challenge_id=challenge_id).all()
        
        # Calculate metrics
        initial_balance = float(challenge.initial_balance)
        current_balance = float(challenge.current_balance)
        max_balance = float(challenge.max_balance or initial_balance)
        
        # Calculate profit
        profit = current_balance - initial_balance
        profit_percentage = (profit / initial_balance) * 100
        
        # Calculate drawdown
        drawdown = ((max_balance - current_balance) / max_balance) * 100
        
        # Check if profit target is met
        profit_target = float(challenge.profit_target)
        profit_target_met = profit >= profit_target
        
        # Check if minimum trading days are met
        min_days = challenge.min_trading_days or 5
        trading_days = challenge.trading_days or 0
        days_requirement_met = trading_days >= min_days
        
        # Check if drawdown limits are violated
        max_drawdown = float(challenge.max_total_drawdown)
        drawdown_violated = drawdown > max_drawdown
        
        # Determine challenge outcome
        if drawdown_violated:
            challenge.status = 'failed'
            challenge.failure_reason = f'Maximum drawdown exceeded: {drawdown:.2f}%'
            challenge.completed_at = datetime.utcnow()
        elif profit_target_met and days_requirement_met:
            # Check if this is a two-phase challenge
            program = Program.query.get(challenge.program_id)
            
            if program.type == 'two_phase' and challenge.phase == 1:
                # Move to phase 2
                challenge.phase = 2
                challenge.profit_target = program.profit_target  # Reset for phase 2
                challenge.trading_days = 0  # Reset trading days
                message = 'Phase 1 completed! Moving to Phase 2'
            else:
                # Challenge completed successfully
                challenge.status = 'completed'
                challenge.completed_at = datetime.utcnow()
                message = 'Challenge completed successfully! Awaiting funding'
        else:
            message = f'Challenge in progress. Profit: {profit_percentage:.2f}%, Days: {trading_days}/{min_days}'
        
        db.session.commit()
        
        return jsonify({
            'message': message,
            'challenge': {
                'id': challenge.id,
                'status': challenge.status,
                'phase': challenge.phase,
                'profit': profit,
                'profit_percentage': round(profit_percentage, 2),
                'drawdown': round(drawdown, 2),
                'trading_days': trading_days,
                'profit_target_met': profit_target_met,
                'days_requirement_met': days_requirement_met
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@challenges_bp.route('/<int:challenge_id>/fund', methods=['POST'])
@token_required
@admin_required
def fund_challenge(challenge_id):
    """Fund a completed challenge"""
    try:
        challenge = Challenge.query.get_or_404(challenge_id)
        
        if challenge.status != 'completed':
            return jsonify({'error': 'Challenge must be completed first'}), 400
        
        # Update challenge status to funded
        challenge.status = 'funded'
        challenge.funded_at = datetime.utcnow()
        
        # Reset balance for funded account
        program = Program.query.get(challenge.program_id)
        challenge.initial_balance = program.account_size
        challenge.current_balance = program.account_size
        challenge.max_balance = program.account_size
        
        db.session.commit()
        
        # TODO (Phase 4 - Email Notifications): Send funding notification email to trader
        # TODO (Phase 12 - MT4/MT5 Integration): Provision MT5 account automatically
        
        return jsonify({
            'message': 'Challenge funded successfully',
            'challenge': {
                'id': challenge.id,
                'status': challenge.status,
                'funded_at': challenge.funded_at.isoformat(),
                'initial_balance': float(challenge.initial_balance)
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@challenges_bp.route('/<int:challenge_id>/trades', methods=['POST'])
@token_required
def add_trade(challenge_id):
    """Add a trade to a challenge (for testing/simulation)"""
    try:
        user_id = g.current_user.id
        
        challenge = Challenge.query.filter_by(
            id=challenge_id,
            user_id=user_id
        ).first_or_404()
        
        if challenge.status not in ['active', 'funded']:
            return jsonify({'error': 'Challenge is not active'}), 400
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['symbol', 'type', 'lots', 'open_price', 'close_price']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Calculate profit and pips
        lots = float(data['lots'])
        open_price = float(data['open_price'])
        close_price = float(data['close_price'])
        
        # Simple profit calculation (needs to be more sophisticated for real trading)
        if data['type'] == 'buy':
            pips = (close_price - open_price) * 10000  # For forex
            profit = pips * lots * 10  # Simplified
        else:  # sell
            pips = (open_price - close_price) * 10000
            profit = pips * lots * 10
        
        # Create trade
        trade = Trade(
            challenge_id=challenge_id,
            symbol=data['symbol'],
            trade_type=data['type'],
            lots=lots,
            open_price=open_price,
            close_price=close_price,
            profit=profit,
            pips=pips,
            open_time=datetime.fromisoformat(data['open_time']) if 'open_time' in data else datetime.utcnow(),
            close_time=datetime.fromisoformat(data['close_time']) if 'close_time' in data else datetime.utcnow(),
            commission=data.get('commission', 0),
            swap=data.get('swap', 0)
        )
        
        db.session.add(trade)
        
        # Update challenge balance
        challenge.current_balance = float(challenge.current_balance) + profit
        
        # Update max balance if needed
        if challenge.current_balance > challenge.max_balance:
            challenge.max_balance = challenge.current_balance
        
        # Increment trading days (simplified - should check if it's a new day)
        if not challenge.trading_days:
            challenge.trading_days = 1
        
        db.session.commit()
        
        return jsonify({
            'message': 'Trade added successfully',
            'trade': {
                'id': trade.id,
                'symbol': trade.symbol,
                'type': trade.trade_type,
                'profit': float(trade.profit),
                'pips': float(trade.pips)
            },
            'challenge': {
                'current_balance': float(challenge.current_balance)
            }
        }), 201
        
    except ValueError as e:
        return jsonify({'error': f'Invalid data: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@challenges_bp.route('/admin/all', methods=['GET'])
@token_required
@admin_required
def get_all_challenges():
    """Get all challenges (admin only)"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        
        # Build query
        query = Challenge.query
        
        if status:
            query = query.filter_by(status=status)
        
        # Paginate
        pagination = query.order_by(desc(Challenge.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'challenges': [{
                'id': challenge.id,
                'user_id': challenge.user_id,
                'program_id': challenge.program_id,
                'status': challenge.status,
                'phase': challenge.phase,
                'initial_balance': float(challenge.initial_balance),
                'current_balance': float(challenge.current_balance),
                'profit_target': float(challenge.profit_target),
                'trading_days': challenge.trading_days,
                'created_at': challenge.created_at.isoformat(),
                'started_at': challenge.started_at.isoformat() if challenge.started_at else None,
                'completed_at': challenge.completed_at.isoformat() if challenge.completed_at else None
            } for challenge in pagination.items],
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@challenges_bp.route('/admin/<int:challenge_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_challenge(challenge_id):
    """Delete a challenge (admin only)"""
    try:
        challenge = Challenge.query.get_or_404(challenge_id)
        
        # Don't allow deleting funded challenges
        if challenge.status == 'funded':
            return jsonify({'error': 'Cannot delete funded challenges'}), 400
        
        # Delete associated trades first
        Trade.query.filter_by(challenge_id=challenge_id).delete()
        
        # Delete challenge
        db.session.delete(challenge)
        db.session.commit()
        
        return jsonify({'message': 'Challenge deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

