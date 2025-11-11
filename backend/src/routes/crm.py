"""
CRM routes for lead management
"""
from flask import Blueprint, request, jsonify, g
from src.database import db
from src.models.lead import Lead, LeadActivity, LeadNote
from src.models.user import User
from src.utils.decorators import token_required
from src.utils.permissions import PermissionManager
from datetime import datetime, timedelta
from sqlalchemy import or_, func
import logging

crm_bp = Blueprint('crm', __name__)
logger = logging.getLogger(__name__)


@crm_bp.route('/leads', methods=['GET'])
@token_required
def get_leads():
    """Get all leads with filtering"""
    try:
        current_user = g.current_user
        
        # Check permission
        if not PermissionManager.can_access_crm(current_user):
            return jsonify({'error': 'Access denied'}), 403
        
        # Get filters
        status = request.args.get('status')
        source = request.args.get('source')
        assigned_to = request.args.get('assigned_to')
        search = request.args.get('search', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Build query
        query = Lead.query
        
        # Apply permission filter
        query = PermissionManager.filter_leads_by_permission(current_user, query)
        
        # Apply filters
        if status:
            query = query.filter_by(status=status)
        
        if source:
            query = query.filter_by(source=source)
        
        if assigned_to:
            query = query.filter_by(assigned_to=int(assigned_to))
        
        if search:
            query = query.filter(
                or_(
                    Lead.first_name.ilike(f'%{search}%'),
                    Lead.last_name.ilike(f'%{search}%'),
                    Lead.email.ilike(f'%{search}%'),
                    Lead.phone.ilike(f'%{search}%')
                )
            )
        
        # Order by score (high to low) and created date
        query = query.order_by(Lead.score.desc(), Lead.created_at.desc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        leads = []
        for lead in pagination.items:
            lead_data = lead.to_dict()
            
            # Add assigned user info
            if lead.assigned_to:
                assigned_user = User.query.get(lead.assigned_to)
                if assigned_user:
                    lead_data['assigned_user'] = {
                        'id': assigned_user.id,
                        'name': f"{assigned_user.first_name} {assigned_user.last_name}",
                        'email': assigned_user.email
                    }
            
            leads.append(lead_data)
        
        return jsonify({
            'leads': leads,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@crm_bp.route('/leads', methods=['POST'])
@token_required
def create_lead():
    """Create new lead"""
    try:
        logger.info('=== CREATE LEAD START ===')
        current_user = g.current_user
        logger.info(f'Current user: {current_user.id} - {current_user.email}')
        
        if not PermissionManager.can_manage_leads(current_user):
            logger.warning('Access denied')
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        logger.info(f'Request data: {data}')
        
        # Validate required fields
        required = ['first_name', 'last_name', 'email']
        for field in required:
            if field not in data:
                logger.warning(f'Missing required field: {field}')
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if lead exists
        existing = Lead.query.filter_by(email=data['email']).first()
        if existing:
            logger.warning(f'Lead already exists: {data["email"]}')
            return jsonify({'error': 'Lead with this email already exists'}), 400
        
        # Process budget
        budget = None
        if data.get('budget'):
            try:
                budget = float(data.get('budget'))
            except (ValueError, TypeError):
                logger.warning(f'Invalid budget value: {data.get("budget")}')
                budget = None
        
        # Create lead
        logger.info('Creating Lead object...')
        lead = Lead(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data.get('phone'),
            country_code=data.get('country_code'),
            source=data.get('source', 'manual'),
            status=data.get('status', 'new'),
            assigned_to=data.get('assigned_to', current_user.id),
            assigned_at=datetime.utcnow(),
            interested_program_id=data.get('interested_program_id'),
            budget=budget,
            company=data.get('company'),
            job_title=data.get('job_title'),
            notes=data.get('notes'),
            tags=data.get('tags', '')
        )
        
        logger.info('Adding lead to session...')
        db.session.add(lead)
        logger.info('Flushing session...')
        db.session.flush()
        logger.info(f'Lead flushed with ID: {lead.id}')
        
        # Calculate score
        logger.info('Calculating score...')
        lead.calculate_score()
        logger.info(f'Score calculated: {lead.score}')
        
        # Create activity
        logger.info('Creating activity...')
        activity = LeadActivity(
            lead_id=lead.id,
            user_id=current_user.id,
            activity_type='note',
            subject='Lead created',
            description=f'Lead created by {current_user.first_name} {current_user.last_name}'
        )
        db.session.add(activity)
        logger.info('Committing transaction...')
        db.session.commit()
        logger.info('=== CREATE LEAD SUCCESS ===')
        
        return jsonify({
            'message': 'Lead created successfully',
            'lead': lead.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f'=== CREATE LEAD ERROR: {str(e)} ===')
        logger.exception(e)
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
