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

crm_bp = Blueprint('crm', __name__)


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
        current_user = g.current_user
        
        if not PermissionManager.can_manage_leads(current_user):
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required = ['first_name', 'last_name', 'email']
        for field in required:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if lead exists
        existing = Lead.query.filter_by(email=data['email']).first()
        if existing:
            return jsonify({'error': 'Lead with this email already exists'}), 400
        
        # Create lead
        lead = Lead(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data.get('phone'),
            country_code=data.get('country_code'),
            source=data.get('source', 'manual'),
            assigned_to=data.get('assigned_to', current_user.id),
            assigned_at=datetime.utcnow(),
            interested_program_id=data.get('interested_program_id'),
            budget=data.get('budget'),
            company=data.get('company'),
            job_title=data.get('job_title'),
            notes=data.get('notes'),
            tags=data.get('tags', '')
        )
        
        db.session.add(lead)
        db.session.flush()
        
        # Calculate score
        lead.calculate_score()
        
        # Create activity
        activity = LeadActivity(
            lead_id=lead.id,
            user_id=current_user.id,
            activity_type='note',
            subject='Lead created',
            description=f'Lead created by {current_user.first_name} {current_user.last_name}'
        )
        db.session.add(activity)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Lead created successfully',
            'lead': lead.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@crm_bp.route('/leads/<int:lead_id>', methods=['GET'])
@token_required
def get_lead(lead_id):
    """Get lead details"""
    try:
        current_user = g.current_user
        
        if not PermissionManager.can_access_crm(current_user):
            return jsonify({'error': 'Access denied'}), 403
        
        lead = Lead.query.get(lead_id)
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404
        
        # Check permission
        viewable_ids = PermissionManager.get_viewable_user_ids(current_user)
        if lead.assigned_to and lead.assigned_to not in viewable_ids:
            return jsonify({'error': 'Access denied'}), 403
        
        lead_data = lead.to_dict()
        
        # Add assigned user
        if lead.assigned_to:
            assigned_user = User.query.get(lead.assigned_to)
            if assigned_user:
                lead_data['assigned_user'] = {
                    'id': assigned_user.id,
                    'name': f"{assigned_user.first_name} {assigned_user.last_name}",
                    'email': assigned_user.email
                }
        
        # Add activities
        activities = LeadActivity.query.filter_by(lead_id=lead_id).order_by(LeadActivity.created_at.desc()).limit(50).all()
        lead_data['activities'] = [a.to_dict() for a in activities]
        
        # Add notes
        notes = LeadNote.query.filter_by(lead_id=lead_id).order_by(LeadNote.created_at.desc()).all()
        lead_data['notes'] = [n.to_dict() for n in notes]
        
        return jsonify(lead_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@crm_bp.route('/leads/<int:lead_id>', methods=['PUT'])
@token_required
def update_lead(lead_id):
    """Update lead"""
    try:
        current_user = g.current_user
        
        if not PermissionManager.can_manage_leads(current_user):
            return jsonify({'error': 'Access denied'}), 403
        
        lead = Lead.query.get(lead_id)
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404
        
        data = request.get_json()
        
        # Track changes for activity log
        changes = []
        
        # Update fields
        if 'first_name' in data:
            lead.first_name = data['first_name']
        if 'last_name' in data:
            lead.last_name = data['last_name']
        if 'email' in data:
            lead.email = data['email']
        if 'phone' in data:
            lead.phone = data['phone']
        if 'country_code' in data:
            lead.country_code = data['country_code']
        
        if 'status' in data:
            old_status = lead.status
            lead.status = data['status']
            changes.append(f"Status: {old_status} → {data['status']}")
        
        if 'source' in data:
            lead.source = data['source']
        
        if 'assigned_to' in data:
            old_assigned = lead.assigned_to
            lead.assigned_to = data['assigned_to']
            lead.assigned_at = datetime.utcnow()
            changes.append(f"Assigned to user {data['assigned_to']}")
        
        if 'interested_program_id' in data:
            lead.interested_program_id = data['interested_program_id']
        if 'budget' in data:
            lead.budget = data['budget']
        if 'company' in data:
            lead.company = data['company']
        if 'job_title' in data:
            lead.job_title = data['job_title']
        if 'notes' in data:
            lead.notes = data['notes']
        if 'tags' in data:
            lead.tags = data['tags']
        if 'next_follow_up' in data:
            lead.next_follow_up = datetime.fromisoformat(data['next_follow_up'])
        
        lead.updated_at = datetime.utcnow()
        
        # Recalculate score
        lead.calculate_score()
        
        # Log activity if there were changes
        if changes:
            activity = LeadActivity(
                lead_id=lead.id,
                user_id=current_user.id,
                activity_type='status_change',
                subject='Lead updated',
                description='; '.join(changes)
            )
            db.session.add(activity)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Lead updated successfully',
            'lead': lead.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@crm_bp.route('/leads/<int:lead_id>/activities', methods=['POST'])
@token_required
def add_lead_activity(lead_id):
    """Add activity to lead"""
    try:
        current_user = g.current_user
        
        if not PermissionManager.can_manage_leads(current_user):
            return jsonify({'error': 'Access denied'}), 403
        
        lead = Lead.query.get(lead_id)
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404
        
        data = request.get_json()
        
        # Create activity
        activity = LeadActivity(
            lead_id=lead_id,
            user_id=current_user.id,
            activity_type=data.get('activity_type', 'note'),
            subject=data.get('subject'),
            description=data.get('description'),
            outcome=data.get('outcome'),
            scheduled_at=datetime.fromisoformat(data['scheduled_at']) if 'scheduled_at' in data else None
        )
        
        db.session.add(activity)
        
        # Update last contacted
        if data.get('activity_type') in ['call', 'email', 'meeting']:
            lead.last_contacted_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Activity added successfully',
            'activity': activity.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@crm_bp.route('/leads/<int:lead_id>/notes', methods=['POST'])
@token_required
def add_lead_note(lead_id):
    """Add note to lead"""
    try:
        current_user = g.current_user
        
        if not PermissionManager.can_manage_leads(current_user):
            return jsonify({'error': 'Access denied'}), 403
        
        lead = Lead.query.get(lead_id)
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404
        
        data = request.get_json()
        
        note = LeadNote(
            lead_id=lead_id,
            user_id=current_user.id,
            content=data['content'],
            is_important=data.get('is_important', False)
        )
        
        db.session.add(note)
        db.session.commit()
        
        return jsonify({
            'message': 'Note added successfully',
            'note': note.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@crm_bp.route('/leads/<int:lead_id>/convert', methods=['POST'])
@token_required
def convert_lead(lead_id):
    """Convert lead to user"""
    try:
        current_user = g.current_user
        
        if not PermissionManager.can_manage_leads(current_user):
            return jsonify({'error': 'Access denied'}), 403
        
        lead = Lead.query.get(lead_id)
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404
        
        if lead.status == 'converted':
            return jsonify({'error': 'Lead already converted'}), 400
        
        data = request.get_json()
        
        # Create user
        new_user = User(
            email=lead.email,
            first_name=lead.first_name,
            last_name=lead.last_name,
            phone=lead.phone,
            country_code=lead.country_code,
            role=data.get('role', 'trader'),
            parent_id=current_user.id,
            level=current_user.level + 1,
            is_active=True,
            is_verified=data.get('email_verified', False)
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.flush()
        
        # Update tree path
        new_user.update_tree_path()
        
        # Mark lead as converted
        lead.convert_to_user(new_user.id)
        
        # Create activity
        activity = LeadActivity(
            lead_id=lead_id,
            user_id=current_user.id,
            activity_type='status_change',
            subject='Lead converted',
            description=f'Lead converted to user (ID: {new_user.id})'
        )
        db.session.add(activity)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Lead converted successfully',
            'user': new_user.to_dict(),
            'lead': lead.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@crm_bp.route('/leads/<int:lead_id>/lost', methods=['POST'])
@token_required
def mark_lead_lost(lead_id):
    """Mark lead as lost"""
    try:
        current_user = g.current_user
        
        if not PermissionManager.can_manage_leads(current_user):
            return jsonify({'error': 'Access denied'}), 403
        
        lead = Lead.query.get(lead_id)
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404
        
        data = request.get_json()
        
        lead.mark_as_lost(
            reason=data['reason'],
            notes=data.get('notes')
        )
        
        # Create activity
        activity = LeadActivity(
            lead_id=lead_id,
            user_id=current_user.id,
            activity_type='status_change',
            subject='Lead marked as lost',
            description=f"Reason: {data['reason']}"
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'message': 'Lead marked as lost',
            'lead': lead.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@crm_bp.route('/stats', methods=['GET'])
@token_required
def get_crm_stats():
    """Get CRM statistics"""
    try:
        current_user = g.current_user
        
        if not PermissionManager.can_access_crm(current_user):
            return jsonify({'error': 'Access denied'}), 403
        
        # Base query with permissions
        base_query = Lead.query
        base_query = PermissionManager.filter_leads_by_permission(current_user, base_query)
        
        # Total leads
        total = base_query.count()
        
        # By status
        by_status = {}
        for status in ['new', 'contacted', 'qualified', 'negotiating', 'converted', 'lost']:
            count = base_query.filter_by(status=status).count()
            by_status[status] = count
        
        # By source
        by_source = {}
        sources = db.session.query(Lead.source, func.count(Lead.id)).group_by(Lead.source).all()
        for source, count in sources:
            by_source[source] = count
        
        # This month
        first_day = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        this_month = base_query.filter(Lead.created_at >= first_day).count()
        
        # Converted this month
        converted_this_month = base_query.filter(
            Lead.status == 'converted',
            Lead.converted_at >= first_day
        ).count()
        
        # Conversion rate
        qualified = base_query.filter_by(status='qualified').count()
        converted = base_query.filter_by(status='converted').count()
        conversion_rate = (converted / qualified * 100) if qualified > 0 else 0
        
        return jsonify({
            'total_leads': total,
            'by_status': by_status,
            'by_source': by_source,
            'this_month': this_month,
            'converted_this_month': converted_this_month,
            'conversion_rate': round(conversion_rate, 2)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@crm_bp.route('/pipeline', methods=['GET'])
@token_required
def get_pipeline():
    """Get sales pipeline view"""
    try:
        current_user = g.current_user
        
        if not PermissionManager.can_access_crm(current_user):
            return jsonify({'error': 'Access denied'}), 403
        
        # Get leads by stage
        base_query = Lead.query
        base_query = PermissionManager.filter_leads_by_permission(current_user, base_query)
        
        pipeline = {}
        stages = ['new', 'contacted', 'qualified', 'negotiating']
        
        for stage in stages:
            leads = base_query.filter_by(status=stage).order_by(Lead.score.desc()).limit(20).all()
            pipeline[stage] = [l.to_dict() for l in leads]
        
        return jsonify(pipeline), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

