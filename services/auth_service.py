"""
Authentication service for CypherD Wallet Backend
BULLETPROOF user authentication and management
"""

from flask_jwt_extended import create_access_token, create_refresh_token
from models.database import User, db
from utils.crypto_utils import crypto_utils
import logging
import re

logger = logging.getLogger(__name__)

class AuthService:
    """Service class for authentication operations"""
    
    def __init__(self):
        self.crypto_utils = crypto_utils
    
    def validate_email(self, email):
        """Validate email format"""
        if not email:
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password(self, password):
        """Validate password strength"""
        if not password or len(password) < 8:
            return False
        
        # Check for at least one uppercase, lowercase, digit, and special character
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        return has_upper and has_lower and has_digit and has_special
    
    def signup(self, email, password, first_name=None, last_name=None):
        """Create a new user account"""
        try:
            # Validate inputs
            if not self.validate_email(email):
                return {
                    'success': False,
                    'error': 'Invalid email format'
                }
            
            if not self.validate_password(password):
                return {
                    'success': False,
                    'error': 'Password must be at least 8 characters with uppercase, lowercase, digit, and special character'
                }
            
            # Check if user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return {
                    'success': False,
                    'error': 'User with this email already exists'
                }
            
            # Create new user
            user = User(
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.set_password(password)
            
            # Save to database
            db.session.add(user)
            db.session.commit()
            
            # Create tokens
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            
            return {
                'success': True,
                'message': 'User created successfully',
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Signup error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to create user: {str(e)}'
            }
    
    def signin(self, email, password):
        """Authenticate user and return tokens"""
        try:
            # Validate inputs
            if not email or not password:
                return {
                    'success': False,
                    'error': 'Email and password are required'
                }
            
            # Find user
            user = User.query.filter_by(email=email).first()
            if not user:
                return {
                    'success': False,
                    'error': 'Invalid email or password'
                }
            
            # Check password
            if not user.check_password(password):
                return {
                    'success': False,
                    'error': 'Invalid email or password'
                }
            
            # Check if user is active
            if not user.is_active:
                return {
                    'success': False,
                    'error': 'Account is deactivated'
                }
            
            # Create tokens
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            
            return {
                'success': True,
                'message': 'Login successful',
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            
        except Exception as e:
            logger.error(f"Signin error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to authenticate user: {str(e)}'
            }
    
    def get_user_profile(self, user_id):
        """Get user profile by ID"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {
                    'success': False,
                    'error': 'User not found'
                }
            
            return {
                'success': True,
                'user': user.to_dict()
            }
            
        except Exception as e:
            logger.error(f"Get user profile error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to get user profile: {str(e)}'
            }
    
    def update_user_profile(self, user_id, **kwargs):
        """Update user profile"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {
                    'success': False,
                    'error': 'User not found'
                }
            
            # Update allowed fields
            allowed_fields = ['first_name', 'last_name', 'phone_number']
            for field, value in kwargs.items():
                if field in allowed_fields and value is not None:
                    setattr(user, field, value)
            
            # Save changes
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Profile updated successfully',
                'user': user.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Update user profile error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to update profile: {str(e)}'
            }
    
    def change_password(self, user_id, current_password, new_password):
        """Change user password"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {
                    'success': False,
                    'error': 'User not found'
                }
            
            # Verify current password
            if not user.check_password(current_password):
                return {
                    'success': False,
                    'error': 'Current password is incorrect'
                }
            
            # Validate new password
            if not self.validate_password(new_password):
                return {
                    'success': False,
                    'error': 'New password must be at least 8 characters with uppercase, lowercase, digit, and special character'
                }
            
            # Update password
            user.set_password(new_password)
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Password changed successfully'
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Change password error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to change password: {str(e)}'
            }

# Global instance
auth_service = AuthService()
