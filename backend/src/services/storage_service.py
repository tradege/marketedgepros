"""
Storage Service using DigitalOcean Spaces (S3-compatible)
Handles file uploads for KYC documents and other assets
"""
import os
import boto3
from botocore.exceptions import ClientError
from flask import current_app
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class StorageService:
    """Storage service for uploading files to DigitalOcean Spaces"""
    
    def __init__(self):
        self.spaces_key = os.getenv('DO_SPACES_KEY') or os.getenv('SPACES_ACCESS_KEY')
        self.spaces_secret = os.getenv('DO_SPACES_SECRET') or os.getenv('SPACES_SECRET_KEY')
        self.spaces_name = os.getenv('DO_SPACES_BUCKET') or os.getenv('SPACES_NAME', 'marketedgepros-storage')
        self.spaces_region = os.getenv('DO_SPACES_REGION') or os.getenv('SPACES_REGION', 'ams3')
        self.spaces_endpoint = f'https://{self.spaces_region}.digitaloceanspaces.com'
        self.cdn_endpoint = f'https://{self.spaces_name}.{self.spaces_region}.cdn.digitaloceanspaces.com'
        
        if not self.spaces_key or not self.spaces_secret:
            logger.warning("DigitalOcean Spaces credentials not configured. Files will be stored locally.")
            self.client = None
        else:
            try:
                self.client = boto3.client(
                    's3',
                    region_name=self.spaces_region,
                    endpoint_url=self.spaces_endpoint,
                    aws_access_key_id=self.spaces_key,
                    aws_secret_access_key=self.spaces_secret
                )
                logger.info(f"DigitalOcean Spaces client initialized: {self.spaces_name}")
            except Exception as e:
                logger.error(f"Failed to initialize Spaces client: {str(e)}")
                self.client = None
    
    def upload_file(self, file, folder='uploads', filename=None, make_public=False):
        """
        Upload a file to DigitalOcean Spaces
        
        Args:
            file: File object from request.files
            folder (str): Folder path in the bucket (e.g., 'kyc', 'profiles')
            filename (str): Custom filename (optional, will generate UUID if not provided)
            make_public (bool): Make file publicly accessible
        
        Returns:
            dict: {'success': bool, 'url': str, 'key': str} or {'success': False, 'error': str}
        """
        try:
            if not self.client:
                # Fallback to local storage
                return self._upload_local(file, folder, filename)
            
            # Generate unique filename if not provided
            if not filename:
                ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'bin'
                filename = f"{uuid.uuid4().hex}.{ext}"
            
            # Create full key (path in bucket)
            key = f"{folder}/{filename}"
            
            # Determine content type
            content_type = file.content_type or 'application/octet-stream'
            
            # Upload to Spaces
            extra_args = {
                'ContentType': content_type,
            }
            
            if make_public:
                extra_args['ACL'] = 'public-read'
            
            self.client.upload_fileobj(
                file,
                self.spaces_name,
                key,
                ExtraArgs=extra_args
            )
            
            # Generate URL (use CDN if available)
            if make_public:
                url = f"{self.cdn_endpoint}/{key}"
            else:
                # Generate presigned URL (valid for 1 hour)
                url = self.client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': self.spaces_name, 'Key': key},
                    ExpiresIn=3600
                )
            
            logger.info(f"File uploaded successfully: {key}")
            
            return {
                'success': True,
                'url': url,
                'key': key,
                'filename': filename
            }
            
        except ClientError as e:
            logger.error(f"Failed to upload file to Spaces: {str(e)}")
            return {
                'success': False,
                'error': f"Upload failed: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error during file upload: {str(e)}")
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}"
            }
    
    def _upload_local(self, file, folder, filename):
        """Fallback: Upload file to local filesystem"""
        try:
            upload_folder = os.getenv('UPLOAD_FOLDER', '/tmp/uploads')
            full_path = os.path.join(upload_folder, folder)
            
            # Create directory if it doesn't exist
            os.makedirs(full_path, exist_ok=True)
            
            # Generate filename if not provided
            if not filename:
                ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'bin'
                filename = f"{uuid.uuid4().hex}.{ext}"
            
            file_path = os.path.join(full_path, filename)
            file.save(file_path)
            
            logger.info(f"File saved locally: {file_path}")
            
            return {
                'success': True,
                'url': f"/uploads/{folder}/{filename}",
                'key': f"{folder}/{filename}",
                'filename': filename,
                'local': True
            }
            
        except Exception as e:
            logger.error(f"Failed to save file locally: {str(e)}")
            return {
                'success': False,
                'error': f"Local upload failed: {str(e)}"
            }
    
    def delete_file(self, key):
        """
        Delete a file from DigitalOcean Spaces
        
        Args:
            key (str): File key (path) in the bucket
        
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            if not self.client:
                # Try to delete from local storage
                return self._delete_local(key)
            
            self.client.delete_object(
                Bucket=self.spaces_name,
                Key=key
            )
            
            logger.info(f"File deleted successfully: {key}")
            return True
            
        except ClientError as e:
            logger.error(f"Failed to delete file from Spaces: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during file deletion: {str(e)}")
            return False
    
    def _delete_local(self, key):
        """Fallback: Delete file from local filesystem"""
        try:
            upload_folder = os.getenv('UPLOAD_FOLDER', '/tmp/uploads')
            file_path = os.path.join(upload_folder, key)
            
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"File deleted locally: {file_path}")
                return True
            else:
                logger.warning(f"File not found: {file_path}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to delete file locally: {str(e)}")
            return False
    
    def get_file_url(self, key, expires_in=3600):
        """
        Get a presigned URL for a file
        
        Args:
            key (str): File key (path) in the bucket
            expires_in (int): URL expiration time in seconds (default: 1 hour)
        
        Returns:
            str: Presigned URL or None if failed
        """
        try:
            if not self.client:
                # Return local URL
                return f"/uploads/{key}"
            
            url = self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.spaces_name, 'Key': key},
                ExpiresIn=expires_in
            )
            
            return url
            
        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error generating URL: {str(e)}")
            return None
    
    def upload_kyc_document(self, file, user_id, document_type):
        """
        Upload a KYC document
        
        Args:
            file: File object from request.files
            user_id (int): User ID
            document_type (str): Type of document (id_proof, address_proof, etc.)
        
        Returns:
            dict: Upload result with URL and key
        """
        # Create folder structure: kyc/{user_id}/{document_type}
        folder = f"kyc/{user_id}"
        
        # Generate filename with timestamp
        ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'pdf'
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"{document_type}_{timestamp}.{ext}"
        
        # Upload file (not public for security)
        return self.upload_file(file, folder, filename, make_public=False)
    
    def upload_profile_image(self, file, user_id):
        """
        Upload a profile image
        
        Args:
            file: File object from request.files
            user_id (int): User ID
        
        Returns:
            dict: Upload result with URL and key
        """
        folder = f"profiles/{user_id}"
        
        ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
        filename = f"avatar.{ext}"
        
        # Make profile images public
        return self.upload_file(file, folder, filename, make_public=True)


# Create singleton instance
storage_service = StorageService()

