"""
Authentication service with JWT and 2FA support
"""
from src.database import db, get_redis
from src.models import User, EmailVerificationToken, PasswordResetToken
from datetime import datetime, timedelta
from flask import current_app
import secrets


class AuthService:
    """Authentication service"""
    
    @staticmethod
    def register_user(email, password, first_name, last_name, referral_code=None, **kwargs):
        """Register a new user"""
        from src.models import Agent, Referral
        from flask import request
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            raise ValueError('Email already registered')
        
        # Create new user
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **kwargs
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Handle referral code if provided
        if referral_code:
            agent = Agent.query.filter_by(agent_code=referral_code, is_active=True).first()
            if agent:
                # Create referral record
                referral = Referral(
                    agent_id=agent.id,
                    referred_user_id=user.id,
                    referral_code=referral_code,
                    ip_address=request.remote_addr if request else None,
                    user_agent=request.headers.get('User-Agent') if request else None,
                    status='pending'
                )
                db.session.add(referral)
                
                # Update agent stats
                agent.referral_count += 1
                db.session.commit()
                
                # Send email notification to upline (agent owner)
                try:
                    from src.services.email_service import EmailService
                    upline_user = agent.user
                    EmailService.send_new_downline_email(upline_user, user)
                except Exception as e:
                    # Log error but don't fail registration
                    import logging
                    logging.error(f'Failed to send downline notification email: {str(e)}')
        
        # Generate email verification token
        verification_token = EmailVerificationToken(user.id)
        db.session.add(verification_token)
        db.session.commit()
        
        return user, verification_token
    
    @staticmethod
    def login_user(email, password, ip_address=None):
        """Login user with email and password"""
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            raise ValueError('Invalid email or password')
        
        if not user.is_active:
            raise ValueError('Account is deactivated')
        
        # Update last login
        user.last_login_at = datetime.utcnow()
        if ip_address:
            user.last_login_ip = ip_address
        db.session.commit()
        
        return user
    
    @staticmethod
    def verify_2fa(user, token):
        """Verify 2FA token"""
        if not user.two_factor_enabled:
            raise ValueError('2FA is not enabled for this user')
        
        if not user.verify_2fa_token(token):
            raise ValueError('Invalid 2FA token')
        
        return True
    
    @staticmethod
    def enable_2fa(user):
        """Enable 2FA for user"""
        if user.two_factor_enabled:
            raise ValueError('2FA is already enabled')
        
        # Generate secret
        secret = user.generate_2fa_secret()
        db.session.commit()
        
        return user.get_2fa_uri()
    
    @staticmethod
    def confirm_2fa(user, token):
        """Confirm and activate 2FA"""
        if user.two_factor_enabled:
            raise ValueError('2FA is already enabled')
        
        if not user.two_factor_secret:
            raise ValueError('2FA secret not generated')
        
        if not user.verify_2fa_token(token):
            raise ValueError('Invalid 2FA token')
        
        user.two_factor_enabled = True
        db.session.commit()
        
        return True
    
    @staticmethod
    def disable_2fa(user, password):
        """Disable 2FA for user"""
        if not user.check_password(password):
            raise ValueError('Invalid password')
        
        user.two_factor_enabled = False
        user.two_factor_secret = None
        db.session.commit()
        
        return True
    
    @staticmethod
    def verify_email(token_string):
        """Verify email with token (URL-based)"""
        token = EmailVerificationToken.query.filter_by(token=token_string).first()
        
        if not token or not token.is_valid():
            raise ValueError('Invalid or expired token')
        
        user = token.user
        user.is_verified = True
        user.email_verified_at = datetime.utcnow()
        token.mark_as_used()
        
        db.session.commit()
        
        return user
    
    @staticmethod
    def verify_email_with_code(email, code):
        """Verify email with 6-digit code"""
        user = User.query.filter_by(email=email).first()
        
        if not user:
            raise ValueError('User not found')
        
        # Find valid verification token with matching code
        token = EmailVerificationToken.query.filter_by(
            user_id=user.id,
            code=code,
            used=False
        ).order_by(EmailVerificationToken.created_at.desc()).first()
        
        if not token or not token.is_valid():
            raise ValueError('Invalid or expired verification code')
        
        user.is_verified = True
        user.email_verified_at = datetime.utcnow()
        token.mark_as_used()
        
        db.session.commit()
        
        return user
    
    @staticmethod
    def resend_verification_code(email):
        """Resend verification code to email"""
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Don't reveal if email exists
            return None
        
        if user.is_verified:
            raise ValueError('Email is already verified')
        
        # Check if there's a recent unused token (within last 2 minutes)
        recent_token = EmailVerificationToken.query.filter_by(
            user_id=user.id,
            used=False
        ).filter(
            EmailVerificationToken.created_at > datetime.utcnow() - timedelta(minutes=2)
        ).first()
        
        if recent_token:
            # Return existing token instead of creating new one
            return recent_token
        
        # Create new verification token
        verification_token = EmailVerificationToken(user.id)
        db.session.add(verification_token)
        db.session.commit()
        
        return verification_token
    
    @staticmethod
    def request_password_reset(email):
        """Request password reset"""
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Don't reveal if email exists
            return None
        
        # Create reset token
        reset_token = PasswordResetToken(user.id)
        db.session.add(reset_token)
        db.session.commit()
        
        return reset_token
    
    @staticmethod
    def reset_password(token_string, new_password):
        """Reset password with token (URL-based)"""
        token = PasswordResetToken.query.filter_by(token=token_string).first()
        
        if not token or not token.is_valid():
            raise ValueError('Invalid or expired token')
        
        user = token.user
        user.set_password(new_password)
        token.mark_as_used()
        
        db.session.commit()
        
        return user
    
    @staticmethod
    def verify_reset_code(email, code):
        """Verify password reset code"""
        user = User.query.filter_by(email=email).first()
        
        if not user:
            raise ValueError('User not found')
        
        # Find valid reset token with matching code
        token = PasswordResetToken.query.filter_by(
            user_id=user.id,
            code=code,
            used=False
        ).order_by(PasswordResetToken.created_at.desc()).first()
        
        if not token or not token.is_valid():
            raise ValueError('Invalid or expired reset code')
        
        return token
    
    @staticmethod
    def reset_password_with_code(email, code, new_password):
        """Reset password with 6-digit code"""
        user = User.query.filter_by(email=email).first()
        
        if not user:
            raise ValueError('User not found')
        
        # Find valid reset token with matching code
        token = PasswordResetToken.query.filter_by(
            user_id=user.id,
            code=code,
            used=False
        ).order_by(PasswordResetToken.created_at.desc()).first()
        
        if not token or not token.is_valid():
            raise ValueError('Invalid or expired reset code')
        
        user.set_password(new_password)
        token.mark_as_used()
        
        db.session.commit()
        
        return user
    
    @staticmethod
    def refresh_access_token(refresh_token):
        """Refresh access token using refresh token"""
        payload = User.verify_token(refresh_token, token_type='refresh')
        
        if not payload:
            raise ValueError('Invalid refresh token')
        
        user = User.query.get(payload['user_id'])
        
        if not user or not user.is_active:
            raise ValueError('User not found or inactive')
        
        return user.generate_access_token()
    
    @staticmethod
    def revoke_token(token):
        """Revoke a token by adding it to blacklist (Redis + Database)"""
        from src.models.token_blacklist import TokenBlacklist
        import jwt
        
        try:
            # Decode token to get jti and user_id
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=["HS256"]
            )
            
            jti = payload.get('jti')
            user_id = payload.get('user_id')
            token_type = payload.get('type', 'access')
            exp = datetime.fromtimestamp(payload['exp'])
            
            if not jti or not user_id:
                return False
            
            # Add to database blacklist (permanent record)
            TokenBlacklist.revoke_token(jti, token_type, user_id, exp)
            
            # Also add to Redis for fast lookup (optional, for performance)
            redis_client = get_redis()
            if redis_client:
                ttl = int((exp - datetime.utcnow()).total_seconds())
                if ttl > 0:
                    redis_client.setex(f'blacklist:{jti}', ttl, '1')
            
            return True
            
        except Exception as e:
            print(f"Error revoking token: {e}")
            return False
    
    @staticmethod
    def is_token_blacklisted(token):
        """Check if token is blacklisted (checks Redis first, then Database)"""
        from src.models.token_blacklist import TokenBlacklist
        import jwt
        
        try:
            # Decode token to get jti
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=["HS256"],
                options={"verify_exp": False}  # Don't fail on expired tokens
            )
            
            jti = payload.get('jti')
            if not jti:
                return False
            
            # Check Redis first (faster)
            redis_client = get_redis()
            if redis_client and redis_client.exists(f'blacklist:{jti}'):
                return True
            
            # Check database (fallback)
            return TokenBlacklist.is_token_revoked(jti)
            
        except Exception:
            return False

