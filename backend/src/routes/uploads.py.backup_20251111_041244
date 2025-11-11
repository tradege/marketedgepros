"""
File upload routes
"""
from flask import Blueprint, request, jsonify, g, send_from_directory, current_app
from src.services.file_service import FileService
from src.utils.decorators import token_required
from src.database import db
import logging
import os

logger = logging.getLogger(__name__)

uploads_bp = Blueprint('uploads', __name__)


@uploads_bp.route('/kyc', methods=['POST'])
@token_required
def upload_kyc_document():
    """Upload KYC document"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    document_type = request.form.get('document_type', 'id')
    
    try:
        result = FileService.save_kyc_document(
            file,
            g.current_user.id,
            document_type
        )
        
        # Update user KYC status
        if g.current_user.kyc_status == 'pending':
            from datetime import datetime
            g.current_user.kyc_status = 'submitted'
            g.current_user.kyc_submitted_at = datetime.utcnow()
            db.session.commit()
        
        return jsonify({
            'message': 'KYC document uploaded successfully',
            'file': result
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f'KYC upload failed: {str(e)}')
        return jsonify({'error': 'Upload failed'}), 500


@uploads_bp.route('/profile-image', methods=['POST'])
@token_required
def upload_profile_image():
    """Upload profile image"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        result = FileService.save_profile_image(file, g.current_user.id)
        
        return jsonify({
            'message': 'Profile image uploaded successfully',
            'file': result
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f'Profile image upload failed: {str(e)}')
        return jsonify({'error': 'Upload failed'}), 500


@uploads_bp.route('/tenant-logo', methods=['POST'])
@token_required
def upload_tenant_logo():
    """Upload tenant logo (admin only)"""
    if g.current_user.role != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    tenant_id = request.form.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'Tenant ID required'}), 400
    
    try:
        if not FileService.allowed_file(file.filename, 'images'):
            return jsonify({'error': 'Invalid file type. Only images allowed'}), 400
        
        FileService.validate_file_size(file, max_size_mb=2)
        
        result = FileService.save_local_file(
            file,
            subfolder=f'tenants/{tenant_id}',
            custom_filename=f'logo.{file.filename.rsplit(".", 1)[1].lower()}'
        )
        
        # Update tenant logo URL
        from src.models import Tenant
        tenant = Tenant.query.get(tenant_id)
        if tenant:
            tenant.logo_url = result['url']
            db.session.commit()
        
        return jsonify({
            'message': 'Tenant logo uploaded successfully',
            'file': result
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f'Tenant logo upload failed: {str(e)}')
        return jsonify({'error': 'Upload failed'}), 500


@uploads_bp.route('/<path:filename>', methods=['GET'])
def serve_file(filename):
    """Serve uploaded files"""
    try:
        upload_folder = current_app.config.get('UPLOAD_FOLDER', '/tmp/uploads')
        return send_from_directory(upload_folder, filename)
    except Exception as e:
        logger.error(f'File serving failed: {str(e)}')
        return jsonify({'error': 'File not found'}), 404

