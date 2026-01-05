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
def get_leads(current_user):
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
def create_lead(current_user):
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
# Add these endpoints to crm.py

@crm_bp.route('/leads/<int:lead_id>', methods=['GET'])
@token_required
def get_lead_details(current_user, lead_id):
    """Get lead details by ID"""
    try:
        current_user = g.current_user
        
        # Check permission
        if not PermissionManager.can_access_crm(current_user):
            return jsonify({'error': 'Access denied'}), 403
        
        lead = Lead.query.get(lead_id)
        
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404
        
        # Permission already checked via can_access_crm
        
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
        
        # Add activity count
        lead_data['activity_count'] = LeadActivity.query.filter_by(lead_id=lead_id).count()
        lead_data['notes_count'] = LeadNote.query.filter_by(lead_id=lead_id).count()
        
        return jsonify(lead_data), 200
        
    except Exception as e:
        logger.error(f'Error getting lead details: {str(e)}')
        return jsonify({'error': str(e)}), 500


@crm_bp.route('/leads/<int:lead_id>/notes', methods=['GET'])
@token_required
def get_lead_notes(current_user, lead_id):
    """Get all notes for a lead"""
    try:
        current_user = g.current_user
        
        # Check permission
        if not PermissionManager.can_access_crm(current_user):
            return jsonify({'error': 'Access denied'}), 403
        
        lead = Lead.query.get(lead_id)
        
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404
        
        # Permission already checked via can_access_crm
        
        notes = LeadNote.query.filter_by(lead_id=lead_id).order_by(LeadNote.created_at.desc()).all()
        
        notes_data = []
        for note in notes:
            note_data = {
                'id': note.id,
                'content': note.content,
                'created_at': note.created_at.isoformat() if note.created_at else None,
                'created_by': None
            }
            
            # Add creator info
            if note.created_by:
                creator = User.query.get(note.created_by)
                if creator:
                    note_data['created_by'] = f"{creator.first_name} {creator.last_name}"
            
            notes_data.append(note_data)
        
        return jsonify({'notes': notes_data}), 200
        
    except Exception as e:
        logger.error(f'Error getting lead notes: {str(e)}')
        return jsonify({'error': str(e)}), 500


@crm_bp.route('/leads/<int:lead_id>/notes', methods=['POST'])
@token_required
def add_lead_note(current_user, lead_id):
    """Add a note to a lead"""
    try:
        current_user = g.current_user
        
        # Check permission
        if not PermissionManager.can_access_crm(current_user):
            return jsonify({'error': 'Access denied'}), 403
        
        lead = Lead.query.get(lead_id)
        
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404
        
        # Permission already checked via can_access_crm
        
        data = request.get_json()
        content = data.get('content', '').strip()
        
        if not content:
            return jsonify({'error': 'Note content is required'}), 400
        
        # Create note
        note = LeadNote(
            lead_id=lead_id,
            content=content,
            user_id=current_user.id,
            created_at=datetime.utcnow()
        )
        
        db.session.add(note)
        
        # Create activity
        activity = LeadActivity(
            lead_id=lead_id,
            activity_type='note_added',
            description=f'Note added: {content[:50]}...' if len(content) > 50 else f'Note added: {content}',
            user_id=current_user.id,
            created_at=datetime.utcnow()
        )
        
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'message': 'Note added successfully',
            'note': {
                'id': note.id,
                'content': note.content,
                'created_at': note.created_at.isoformat(),
                'created_by': f"{current_user.first_name} {current_user.last_name}"
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error adding lead note: {str(e)}')
        return jsonify({'error': str(e)}), 500


@crm_bp.route('/leads/<int:lead_id>', methods=['PATCH', 'PUT'])
@token_required
def update_lead(current_user, lead_id):
    """Update lead details"""
    try:
        current_user = g.current_user
        
        # Check permission
        if not PermissionManager.can_access_crm(current_user):
            return jsonify({'error': 'Access denied'}), 403
        
        lead = Lead.query.get(lead_id)
        
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404
        
        # Permission already checked via can_access_crm
        
        data = request.get_json()
        
        # Track changes for activity log
        changes = []
        
        # Update allowed fields
        allowed_fields = ['status', 'score', 'budget', 'assigned_to', 'next_followup', 'notes']
        
        for field in allowed_fields:
            if field in data:
                old_value = getattr(lead, field)
                new_value = data[field]
                
                if old_value != new_value:
                    setattr(lead, field, new_value)
                    changes.append(f'{field}: {old_value} → {new_value}')
        
        if changes:
            lead.updated_at = datetime.utcnow()
            
            # Create activity
            activity = LeadActivity(
                lead_id=lead_id,
                activity_type='lead_updated',
                description=f'Lead updated: {", ".join(changes)}',
                user_id=current_user.id,
                created_at=datetime.utcnow()
            )
            
            db.session.add(activity)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Lead updated successfully',
            'lead': lead.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error updating lead: {str(e)}')
        return jsonify({'error': str(e)}), 500


@crm_bp.route('/leads/<int:lead_id>', methods=['DELETE'])
@token_required
def delete_lead(current_user, lead_id):
    """Delete a lead"""
    try:
        current_user = g.current_user
        
        # Check permission - only admins can delete
        if current_user.role not in ['admin', 'supermaster']:
            return jsonify({'error': 'Admin access required'}), 403
        
        lead = Lead.query.get(lead_id)
        
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404
        
        # Delete related records
        LeadNote.query.filter_by(lead_id=lead_id).delete()
        LeadActivity.query.filter_by(lead_id=lead_id).delete()
        
        # Delete lead
        db.session.delete(lead)
        db.session.commit()
        
        return jsonify({'message': 'Lead deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error deleting lead: {str(e)}')
        return jsonify({'error': str(e)}), 500


@crm_bp.route('/leads/<int:lead_id>/activities', methods=['POST'])
@token_required
def add_lead_activity(current_user, lead_id):
    """Add activity to a lead"""
    try:
        current_user = g.current_user
        
        # Check permission
        if not PermissionManager.can_access_crm(current_user):
            return jsonify({'error': 'Access denied'}), 403
        
        lead = Lead.query.get(lead_id)
        
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404
        
        data = request.get_json()
        
        # Validate required fields
        if not data or 'activity_type' not in data:
            return jsonify({'error': 'activity_type is required'}), 400
        
        # Create activity
        activity = LeadActivity(
            lead_id=lead_id,
            user_id=current_user.id,
            activity_type=data.get('activity_type'),
            description=data.get('description', ''),
            metadata=data.get('metadata', {})
        )
        
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'message': 'Activity added successfully',
            'activity': activity.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error adding activity: {str(e)}')
        return jsonify({'error': str(e)}), 500


@crm_bp.route('/leads/<int:lead_id>/convert', methods=['POST'])
@token_required
def convert_lead(current_user, lead_id):
    """Convert lead to customer"""
    try:
        current_user = g.current_user
        
        # Check permission
        if not PermissionManager.can_access_crm(current_user):
            return jsonify({'error': 'Access denied'}), 403
        
        lead = Lead.query.get(lead_id)
        
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404
        
        # Update lead status to converted
        lead.status = 'converted'
        lead.converted_at = datetime.utcnow()
        lead.converted_by = current_user.id
        
        # Add activity
        activity = LeadActivity(
            lead_id=lead_id,
            user_id=current_user.id,
            activity_type='converted',
            description='Lead converted to customer'
        )
        
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'message': 'Lead converted successfully',
            'lead': lead.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error converting lead: {str(e)}')
        return jsonify({'error': str(e)}), 500


@crm_bp.route('/leads/<int:lead_id>/lost', methods=['POST'])
@token_required
def mark_lead_lost(current_user, lead_id):
    """Mark lead as lost"""
    try:
        current_user = g.current_user
        
        # Check permission
        if not PermissionManager.can_access_crm(current_user):
            return jsonify({'error': 'Access denied'}), 403
        
        lead = Lead.query.get(lead_id)
        
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404
        
        data = request.get_json() or {}
        
        # Update lead status to lost
        lead.status = 'lost'
        lead.lost_reason = data.get('reason', '')
        lead.lost_at = datetime.utcnow()
        
        # Add activity
        activity = LeadActivity(
            lead_id=lead_id,
            user_id=current_user.id,
            activity_type='lost',
            description=f"Lead marked as lost: {data.get('reason', 'No reason provided')}"
        )
        
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'message': 'Lead marked as lost',
            'lead': lead.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error marking lead as lost: {str(e)}')
        return jsonify({'error': str(e)}), 500


@crm_bp.route('/stats', methods=['GET'])
@token_required
def get_crm_stats(current_user):
    """Get CRM statistics"""
    try:
        current_user = g.current_user
        
        # Check permission
        if not PermissionManager.can_access_crm(current_user):
            return jsonify({'error': 'Access denied'}), 403
        
        # Build base query with permission filter
        base_query = Lead.query
        base_query = PermissionManager.filter_leads_by_permission(current_user, base_query)
        
        # Get counts by status
        total_leads = base_query.count()
        new_leads = base_query.filter_by(status='new').count()
        contacted_leads = base_query.filter_by(status='contacted').count()
        qualified_leads = base_query.filter_by(status='qualified').count()
        converted_leads = base_query.filter_by(status='converted').count()
        lost_leads = base_query.filter_by(status='lost').count()
        
        # Get conversion rate
        conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0
        
        # Get leads created in last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_leads = base_query.filter(Lead.created_at >= thirty_days_ago).count()
        
        # Get average score
        avg_score = db.session.query(func.avg(Lead.score)).filter(
            Lead.id.in_([l.id for l in base_query.all()])
        ).scalar() or 0
        
        return jsonify({
            'total_leads': total_leads,
            'new_leads': new_leads,
            'contacted_leads': contacted_leads,
            'qualified_leads': qualified_leads,
            'converted_leads': converted_leads,
            'lost_leads': lost_leads,
            'conversion_rate': round(conversion_rate, 2),
            'recent_leads_30d': recent_leads,
            'average_score': round(float(avg_score), 2)
        }), 200
        
    except Exception as e:
        logger.error(f'Error getting CRM stats: {str(e)}')
        return jsonify({'error': str(e)}), 500


@crm_bp.route('/pipeline', methods=['GET'])
@token_required
def get_crm_pipeline(current_user):
    """Get CRM pipeline view"""
    try:
        current_user = g.current_user
        
        # Check permission
        if not PermissionManager.can_access_crm(current_user):
            return jsonify({'error': 'Access denied'}), 403
        
        # Build base query with permission filter
        base_query = Lead.query
        base_query = PermissionManager.filter_leads_by_permission(current_user, base_query)
        
        # Group leads by status
        pipeline = {
            'new': [],
            'contacted': [],
            'qualified': [],
            'proposal': [],
            'negotiation': [],
            'converted': [],
            'lost': []
        }
        
        # Get all leads
        leads = base_query.order_by(Lead.score.desc()).all()
        
        for lead in leads:
            status = lead.status or 'new'
            if status in pipeline:
                lead_data = lead.to_dict()
                
                # Add assigned user info
                if lead.assigned_to:
                    assigned_user = User.query.get(lead.assigned_to)
                    if assigned_user:
                        lead_data['assigned_user'] = {
                            'id': assigned_user.id,
                            'name': f"{assigned_user.first_name} {assigned_user.last_name}"
                        }
                
                pipeline[status].append(lead_data)
        
        # Get counts
        counts = {status: len(leads) for status, leads in pipeline.items()}
        
        return jsonify({
            'pipeline': pipeline,
            'counts': counts
        }), 200
        
    except Exception as e:
        logger.error(f'Error getting pipeline: {str(e)}')
        return jsonify({'error': str(e)}), 500
