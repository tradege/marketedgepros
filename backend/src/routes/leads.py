"""
Leads routes for CRM and course signups
"""
from flask import Blueprint, request, jsonify
from src.database import db
from src.models.lead import Lead
from src.services.email_service import send_course_welcome_email
from src.services.discord_service import discord_service
import logging

logger = logging.getLogger(__name__)

leads_bp = Blueprint('leads', __name__, url_prefix='/leads')


@leads_bp.route('/course-signup', methods=['POST'])
def course_signup():
    """
    Handle free course signup
    """
    try:
        data = request.get_json()
        email = data.get('email')
        name = data.get('name')
        source = data.get('source', 'free_course')
        
        if not email or not name:
            return jsonify({'error': 'Email and name are required'}), 400
        
        # Check if lead already exists
        existing_lead = Lead.query.filter_by(email=email).first()
        
        if existing_lead:
            # Update existing lead
            existing_lead.name = name
            existing_lead.source = source
            existing_lead.status = 'contacted'
        else:
            # Create new lead
            lead = Lead(
                email=email,
                name=name,
                source=source,
                status='new',
                lead_type='course_signup'
            )
            db.session.add(lead)
        
        db.session.commit()
        
        # Send welcome email with course access
        try:
            send_course_welcome_email(email, name)
        except Exception as e:
            logger.error(f"Failed to send course welcome email: {str(e)}")
        
        # Send Discord notification
        try:
            discord_service.send_webhook_notification(
                f"🎓 New course signup: {name} ({email})"
            )
        except Exception as e:
            logger.error(f"Failed to send Discord notification: {str(e)}")
        
        return jsonify({
            'message': 'Successfully signed up for the course',
            'email': email
        }), 201
        
    except Exception as e:
        logger.error(f"Course signup error: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to process signup'}), 500

