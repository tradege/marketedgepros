"""
File upload service with S3 support
"""
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
import logging

logger = logging.getLogger(__name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    'images': {'png', 'jpg', 'jpeg', 'gif', 'webp'},
    'documents': {'pdf', 'doc', 'docx'},
    'all': {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf', 'doc', 'docx'}
}


class FileService:
    """File upload and management service"""
    
    @staticmethod
    def allowed_file(filename, file_type='all'):
        """Check if file extension is allowed"""
        if '.' not in filename:
            return False
        
        ext = filename.rsplit('.', 1)[1].lower()
        return ext in ALLOWED_EXTENSIONS.get(file_type, ALLOWED_EXTENSIONS['all'])
    
    @staticmethod
    def generate_unique_filename(original_filename):
        """Generate unique filename while preserving extension"""
        ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
        unique_name = f"{uuid.uuid4().hex}"
        return f"{unique_name}.{ext}" if ext else unique_name
    
    @staticmethod
    def save_local_file(file, subfolder='uploads', custom_filename=None):
        """Save file to local storage"""
        try:
            # Get upload folder from config
            upload_folder = current_app.config.get('UPLOAD_FOLDER', '/tmp/uploads')
            
            # Create subfolder path
            folder_path = os.path.join(upload_folder, subfolder)
            os.makedirs(folder_path, exist_ok=True)
            
            # Generate filename
            if custom_filename:
                filename = secure_filename(custom_filename)
            else:
                filename = FileService.generate_unique_filename(file.filename)
            
            # Save file
            file_path = os.path.join(folder_path, filename)
            file.save(file_path)
            
            logger.info(f'File saved locally: {file_path}')
            
            return {
                'filename': filename,
                'path': file_path,
                'url': f'/uploads/{subfolder}/{filename}',
                'size': os.path.getsize(file_path)
            }
            
        except Exception as e:
            logger.error(f'Failed to save file locally: {str(e)}')
            raise ValueError(f'File upload failed: {str(e)}')
    
    @staticmethod
    def save_s3_file(file, bucket_name, subfolder='uploads', custom_filename=None):
        """
        Save file to AWS S3
        Note: Requires boto3 and AWS credentials configured
        """
        try:
            import boto3
            from botocore.exceptions import ClientError
            
            # Initialize S3 client
            s3_client = boto3.client('s3')
            
            # Generate filename
            if custom_filename:
                filename = secure_filename(custom_filename)
            else:
                filename = FileService.generate_unique_filename(file.filename)
            
            # Create S3 key (path)
            s3_key = f"{subfolder}/{filename}"
            
            # Upload file
            s3_client.upload_fileobj(
                file,
                bucket_name,
                s3_key,
                ExtraArgs={'ACL': 'public-read'}
            )
            
            # Generate URL
            url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
            
            logger.info(f'File uploaded to S3: {url}')
            
            return {
                'filename': filename,
                'bucket': bucket_name,
                'key': s3_key,
                'url': url
            }
            
        except ImportError:
            logger.error('boto3 not installed. Install with: pip install boto3')
            raise ValueError('S3 upload not available')
        except ClientError as e:
            logger.error(f'S3 upload failed: {str(e)}')
            raise ValueError(f'S3 upload failed: {str(e)}')
        except Exception as e:
            logger.error(f'File upload failed: {str(e)}')
            raise ValueError(f'File upload failed: {str(e)}')
    
    @staticmethod
    def delete_local_file(file_path):
        """Delete file from local storage"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f'File deleted: {file_path}')
                return True
            return False
        except Exception as e:
            logger.error(f'Failed to delete file: {str(e)}')
            return False
    
    @staticmethod
    def delete_s3_file(bucket_name, s3_key):
        """Delete file from S3"""
        try:
            import boto3
            from botocore.exceptions import ClientError
            
            s3_client = boto3.client('s3')
            s3_client.delete_object(Bucket=bucket_name, Key=s3_key)
            
            logger.info(f'File deleted from S3: {s3_key}')
            return True
            
        except ImportError:
            logger.error('boto3 not installed')
            return False
        except ClientError as e:
            logger.error(f'S3 delete failed: {str(e)}')
            return False
        except Exception as e:
            logger.error(f'File deletion failed: {str(e)}')
            return False
    
    @staticmethod
    def validate_file_size(file, max_size_mb=16):
        """Validate file size"""
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        
        max_size_bytes = max_size_mb * 1024 * 1024
        
        if size > max_size_bytes:
            raise ValueError(f'File size exceeds {max_size_mb}MB limit')
        
        return size
    
    @staticmethod
    def save_kyc_document(file, user_id, document_type):
        """Save KYC document for user"""
        try:
            # Validate file
            if not FileService.allowed_file(file.filename, 'documents'):
                raise ValueError('Invalid file type. Only PDF, DOC, DOCX allowed')
            
            # Validate size
            FileService.validate_file_size(file, max_size_mb=10)
            
            # Generate custom filename
            ext = file.filename.rsplit('.', 1)[1].lower()
            custom_filename = f"kyc_{user_id}_{document_type}_{uuid.uuid4().hex[:8]}.{ext}"
            
            # Save file (local or S3)
            # For now, using local storage
            result = FileService.save_local_file(
                file,
                subfolder=f'kyc/{user_id}',
                custom_filename=custom_filename
            )
            
            logger.info(f'KYC document saved for user {user_id}: {document_type}')
            
            return result
            
        except Exception as e:
            logger.error(f'KYC document upload failed: {str(e)}')
            raise ValueError(str(e))
    
    @staticmethod
    def save_profile_image(file, user_id):
        """Save user profile image"""
        try:
            # Validate file
            if not FileService.allowed_file(file.filename, 'images'):
                raise ValueError('Invalid file type. Only images allowed')
            
            # Validate size
            FileService.validate_file_size(file, max_size_mb=5)
            
            # Generate custom filename
            ext = file.filename.rsplit('.', 1)[1].lower()
            custom_filename = f"profile_{user_id}.{ext}"
            
            # Save file
            result = FileService.save_local_file(
                file,
                subfolder=f'profiles',
                custom_filename=custom_filename
            )
            
            logger.info(f'Profile image saved for user {user_id}')
            
            return result
            
        except Exception as e:
            logger.error(f'Profile image upload failed: {str(e)}')
            raise ValueError(str(e))

