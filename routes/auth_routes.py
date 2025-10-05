"""
Authentication routes for CypherD Wallet Backend
BULLETPROOF user authentication endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth_service import auth_service
import logging

logger = logging.getLogger(__name__)

# Create blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    User registration endpoint
    
    Request body:
    {
        "email": "user@example.com",
        "password": "SecurePassword123!",
        "first_name": "John",  # Optional
        "last_name": "Doe"     # Optional
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        
        # Validate required fields
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Create user
        result = auth_service.signup(email, password, first_name, last_name)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Signup endpoint error: {str(e)}")
        return jsonify({'error': f'Signup failed: {str(e)}'}), 500

@auth_bp.route('/signin', methods=['POST'])
def signin():
    """
    User login endpoint
    
    Request body:
    {
        "email": "user@example.com",
        "password": "SecurePassword123!"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        # Validate required fields
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Authenticate user
        result = auth_service.signin(email, password)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 401
            
    except Exception as e:
        logger.error(f"Signin endpoint error: {str(e)}")
        return jsonify({'error': f'Signin failed: {str(e)}'}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get user profile endpoint
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        result = auth_service.get_user_profile(user_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        logger.error(f"Get profile endpoint error: {str(e)}")
        return jsonify({'error': f'Failed to get profile: {str(e)}'}), 500

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """
    Update user profile endpoint
    
    Request body:
    {
        "first_name": "John",     # Optional
        "last_name": "Doe",       # Optional
        "phone_number": "+1234567890"  # Optional
    }
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        # Update profile
        result = auth_service.update_user_profile(user_id, **data)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Update profile endpoint error: {str(e)}")
        return jsonify({'error': f'Failed to update profile: {str(e)}'}), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """
    Change password endpoint
    
    Request body:
    {
        "current_password": "OldPassword123!",
        "new_password": "NewPassword123!"
    }
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        # Validate required fields
        if not current_password or not new_password:
            return jsonify({'error': 'Current password and new password are required'}), 400
        
        # Change password
        result = auth_service.change_password(user_id, current_password, new_password)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Change password endpoint error: {str(e)}")
        return jsonify({'error': f'Failed to change password: {str(e)}'}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token endpoint
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        from flask_jwt_extended import create_access_token
        
        # Create new access token
        new_access_token = create_access_token(identity=user_id)
        
        return jsonify({
            'success': True,
            'access_token': new_access_token
        }), 200
            
    except Exception as e:
        logger.error(f"Refresh token endpoint error: {str(e)}")
        return jsonify({'error': f'Failed to refresh token: {str(e)}'}), 500
