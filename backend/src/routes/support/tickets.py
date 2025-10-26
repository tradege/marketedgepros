"""
Support Tickets API Routes
"""
from flask import Blueprint, request, jsonify, current_app
from sqlalchemy import desc
from src.database import db
from src.models.support_ticket import SupportTicket, TicketMessage
from src.utils.decorators import token_required, admin_required
from src.services.email_service import EmailService
import logging
import json

logger = logging.getLogger(__name__)

tickets_bp = Blueprint('support_tickets', __name__)


# =====================================================
# Public Routes
# =====================================================

@tickets_bp.route('/', methods=['POST'])
def create_ticket():
    """Create new support ticket (public or authenticated)"""
    try:
        data = request.get_json()
        
        # Get user from token if available
        user_id = None
        email = data.get('email')
        name = data.get('name')
        
        # Validate required fields
        if not email or not name:
            return jsonify({'error': 'Email and name are required'}), 400
        
        subject = data.get('subject')
        description = data.get('description')
        category = data.get('category', 'general')
        priority = data.get('priority', 'medium')
        
        if not subject or not description:
            return jsonify({'error': 'Subject and description are required'}), 400
        
        # Create ticket
        ticket = SupportTicket(
            ticket_number=SupportTicket.generate_ticket_number(),
            user_id=user_id,
            email=email,
            name=name,
            subject=subject,
            description=description,
            category=category,
            priority=priority,
            status='open'
        )
        
        # Handle attachments if provided
        if 'attachments' in data and data['attachments']:
            ticket.attachments = json.dumps(data['attachments'])
        
        db.session.add(ticket)
        db.session.commit()
        
        # Send confirmation email
        try:
            EmailService.send_ticket_created_email(ticket)
        except Exception as e:
            logger.error(f"Failed to send ticket confirmation email: {str(e)}")
        
        logger.info(f"Ticket created: {ticket.ticket_number}")
        
        return jsonify({
            'message': 'Support ticket created successfully',
            'ticket': ticket.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating ticket: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to create ticket'}), 500


@tickets_bp.route('/<ticket_number>', methods=['GET'])
def get_ticket_by_number(ticket_number):
    """Get ticket by ticket number (public access with email verification)"""
    try:
        email = request.args.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        ticket = SupportTicket.query.filter_by(ticket_number=ticket_number, email=email).first()
        
        if not ticket:
            return jsonify({'error': 'Ticket not found'}), 404
        
        return jsonify(ticket.to_dict(include_messages=True)), 200
        
    except Exception as e:
        logger.error(f"Error fetching ticket: {str(e)}")
        return jsonify({'error': 'Failed to fetch ticket'}), 500


@tickets_bp.route('/<ticket_number>/messages', methods=['POST'])
def add_ticket_message(ticket_number):
    """Add message to ticket"""
    try:
        data = request.get_json()
        email = data.get('email')
        message_text = data.get('message')
        
        if not email or not message_text:
            return jsonify({'error': 'Email and message are required'}), 400
        
        ticket = SupportTicket.query.filter_by(ticket_number=ticket_number, email=email).first()
        
        if not ticket:
            return jsonify({'error': 'Ticket not found'}), 404
        
        if ticket.status == 'closed':
            return jsonify({'error': 'Cannot add message to closed ticket'}), 400
        
        # Create message
        message = TicketMessage(
            ticket_id=ticket.id,
            email=email,
            name=data.get('name', ticket.name),
            message=message_text,
            is_staff=False
        )
        
        # Handle attachments if provided
        if 'attachments' in data and data['attachments']:
            message.attachments = json.dumps(data['attachments'])
        
        db.session.add(message)
        
        # Update ticket status if it was waiting for customer
        if ticket.status == 'waiting_customer':
            ticket.status = 'in_progress'
        
        db.session.commit()
        
        logger.info(f"Message added to ticket {ticket_number}")
        
        return jsonify({
            'message': 'Message added successfully',
            'ticket_message': message.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error adding message: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to add message'}), 500


# =====================================================
# User Routes (Authenticated)
# =====================================================

@tickets_bp.route('/my', methods=['GET'])
@token_required
def get_my_tickets(current_user):
    """Get current user's tickets"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        
        query = SupportTicket.query.filter_by(user_id=current_user.id)
        
        if status:
            query = query.filter_by(status=status)
        
        pagination = query.order_by(SupportTicket.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'tickets': [ticket.to_dict() for ticket in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_tickets': pagination.total,
                'total_pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching user tickets: {str(e)}")
        return jsonify({'error': 'Failed to fetch tickets'}), 500


@tickets_bp.route('/<int:ticket_id>', methods=['GET'])
@token_required
def get_ticket(current_user, ticket_id):
    """Get ticket by ID (user must own the ticket)"""
    try:
        ticket = SupportTicket.query.get(ticket_id)
        
        if not ticket:
            return jsonify({'error': 'Ticket not found'}), 404
        
        # Check if user owns the ticket
        if ticket.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify(ticket.to_dict(include_messages=True)), 200
        
    except Exception as e:
        logger.error(f"Error fetching ticket: {str(e)}")
        return jsonify({'error': 'Failed to fetch ticket'}), 500


@tickets_bp.route('/<int:ticket_id>/close', methods=['POST'])
@token_required
def close_ticket(current_user, ticket_id):
    """Close ticket"""
    try:
        ticket = SupportTicket.query.get(ticket_id)
        
        if not ticket:
            return jsonify({'error': 'Ticket not found'}), 404
        
        # Check if user owns the ticket
        if ticket.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        ticket.status = 'closed'
        ticket.closed_at = db.func.now()
        db.session.commit()
        
        logger.info(f"Ticket {ticket.ticket_number} closed by user")
        
        return jsonify({
            'message': 'Ticket closed successfully',
            'ticket': ticket.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error closing ticket: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to close ticket'}), 500


@tickets_bp.route('/<int:ticket_id>/rate', methods=['POST'])
@token_required
def rate_ticket(current_user, ticket_id):
    """Rate closed ticket"""
    try:
        data = request.get_json()
        rating = data.get('rating')
        feedback = data.get('feedback', '')
        
        if not rating or rating < 1 or rating > 5:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        ticket = SupportTicket.query.get(ticket_id)
        
        if not ticket:
            return jsonify({'error': 'Ticket not found'}), 404
        
        # Check if user owns the ticket
        if ticket.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        if ticket.status != 'closed':
            return jsonify({'error': 'Can only rate closed tickets'}), 400
        
        ticket.rating = rating
        ticket.feedback = feedback
        db.session.commit()
        
        logger.info(f"Ticket {ticket.ticket_number} rated: {rating} stars")
        
        return jsonify({
            'message': 'Thank you for your feedback',
            'ticket': ticket.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error rating ticket: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to rate ticket'}), 500


# =====================================================
# Admin Routes
# =====================================================

@tickets_bp.route('/admin/all', methods=['GET'])
@admin_required
def get_all_tickets(current_user):
    """Get all tickets (admin only)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        category = request.args.get('category')
        priority = request.args.get('priority')
        assigned_to = request.args.get('assigned_to', type=int)
        
        query = SupportTicket.query
        
        if status:
            query = query.filter_by(status=status)
        if category:
            query = query.filter_by(category=category)
        if priority:
            query = query.filter_by(priority=priority)
        if assigned_to:
            query = query.filter_by(assigned_to=assigned_to)
        
        pagination = query.order_by(
            SupportTicket.priority.desc(),
            SupportTicket.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'tickets': [ticket.to_dict() for ticket in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_tickets': pagination.total,
                'total_pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching tickets: {str(e)}")
        return jsonify({'error': 'Failed to fetch tickets'}), 500


@tickets_bp.route('/admin/<int:ticket_id>/assign', methods=['PUT'])
@admin_required
def assign_ticket(current_user, ticket_id):
    """Assign ticket to staff member"""
    try:
        data = request.get_json()
        assigned_to = data.get('assigned_to')
        
        ticket = SupportTicket.query.get(ticket_id)
        
        if not ticket:
            return jsonify({'error': 'Ticket not found'}), 404
        
        ticket.assigned_to = assigned_to
        if ticket.status == 'open':
            ticket.status = 'in_progress'
        
        db.session.commit()
        
        logger.info(f"Ticket {ticket.ticket_number} assigned to user {assigned_to}")
        
        return jsonify({
            'message': 'Ticket assigned successfully',
            'ticket': ticket.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error assigning ticket: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to assign ticket'}), 500


@tickets_bp.route('/admin/<int:ticket_id>/status', methods=['PUT'])
@admin_required
def update_ticket_status(current_user, ticket_id):
    """Update ticket status"""
    try:
        data = request.get_json()
        status = data.get('status')
        
        if status not in ['open', 'in_progress', 'waiting_customer', 'resolved', 'closed']:
            return jsonify({'error': 'Invalid status'}), 400
        
        ticket = SupportTicket.query.get(ticket_id)
        
        if not ticket:
            return jsonify({'error': 'Ticket not found'}), 404
        
        old_status = ticket.status
        ticket.status = status
        
        # Set timestamps based on status
        if status == 'resolved' and old_status != 'resolved':
            ticket.resolved_at = db.func.now()
        elif status == 'closed' and old_status != 'closed':
            ticket.closed_at = db.func.now()
        
        db.session.commit()
        
        logger.info(f"Ticket {ticket.ticket_number} status updated: {old_status} -> {status}")
        
        return jsonify({
            'message': 'Ticket status updated successfully',
            'ticket': ticket.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error updating ticket status: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to update status'}), 500


@tickets_bp.route('/admin/<int:ticket_id>/reply', methods=['POST'])
@admin_required
def reply_to_ticket(current_user, ticket_id):
    """Add staff reply to ticket"""
    try:
        data = request.get_json()
        message_text = data.get('message')
        is_internal = data.get('is_internal', False)
        
        if not message_text:
            return jsonify({'error': 'Message is required'}), 400
        
        ticket = SupportTicket.query.get(ticket_id)
        
        if not ticket:
            return jsonify({'error': 'Ticket not found'}), 404
        
        # Create message
        message = TicketMessage(
            ticket_id=ticket.id,
            user_id=current_user.id,
            message=message_text,
            is_staff=True,
            is_internal=is_internal
        )
        
        # Handle attachments if provided
        if 'attachments' in data and data['attachments']:
            message.attachments = json.dumps(data['attachments'])
        
        db.session.add(message)
        
        # Set first response time if not set
        if not ticket.first_response_at:
            ticket.first_response_at = db.func.now()
        
        # Update ticket status
        if ticket.status == 'open':
            ticket.status = 'in_progress'
        elif not is_internal:
            ticket.status = 'waiting_customer'
        
        db.session.commit()
        
        # Send email notification to customer if not internal
        if not is_internal:
            try:
                EmailService.send_ticket_reply_email(ticket, message)
            except Exception as e:
                logger.error(f"Failed to send reply notification email: {str(e)}")
        
        logger.info(f"Staff reply added to ticket {ticket.ticket_number}")
        
        return jsonify({
            'message': 'Reply added successfully',
            'ticket_message': message.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error adding reply: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to add reply'}), 500

