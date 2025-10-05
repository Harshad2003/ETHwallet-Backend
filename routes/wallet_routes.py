"""
Wallet routes for CypherD Wallet Backend
BULLETPROOF wallet management endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.wallet_service import wallet_service
from services.price_service import price_service
from services.email_service import email_service
from utils.crypto_utils import crypto_utils
import logging

logger = logging.getLogger(__name__)

# Create blueprint
wallet_bp = Blueprint('wallet', __name__)

@wallet_bp.route('/create', methods=['POST'])
@jwt_required()
def create_wallet():
    """
    Create a new wallet for the authenticated user
    
    Request body:
    {
        "wallet_name": "My Wallet",  # Optional
        "is_primary": true  # Optional, defaults to false
    }
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json() or {}
        wallet_name = data.get('wallet_name')
        is_primary = data.get('is_primary', False)
        
        # Create wallet
        result = wallet_service.create_wallet(
            user_id=user_id,
            wallet_name=wallet_name,
            is_primary=is_primary
        )
        
        if result['success']:
            # Send email notification
            try:
                from models.database import User
                user = User.query.get(user_id)
                if user and user.email:
                    email_service.send_wallet_created_notification(
                        user.email, 
                        result['wallet']
                    )
            except Exception as e:
                logger.warning(f"Failed to send wallet creation email: {str(e)}")
            
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Create wallet endpoint error: {str(e)}")
        return jsonify({'error': f'Failed to create wallet: {str(e)}'}), 500

@wallet_bp.route('/import', methods=['POST'])
@jwt_required()
def import_wallet():
    """
    Import an existing wallet using mnemonic phrase
    
    Request body:
    {
        "mnemonic": "word1 word2 ... word12",
        "wallet_name": "Imported Wallet",  # Optional
        "is_primary": true  # Optional, defaults to false
    }
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        mnemonic = data.get('mnemonic')
        if not mnemonic:
            return jsonify({'error': 'Mnemonic phrase is required'}), 400
        
        wallet_name = data.get('wallet_name')
        is_primary = data.get('is_primary', False)
        
        # Import wallet
        result = wallet_service.import_wallet(
            user_id=user_id,
            mnemonic=mnemonic,
            wallet_name=wallet_name,
            is_primary=is_primary
        )
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Import wallet endpoint error: {str(e)}")
        return jsonify({'error': f'Failed to import wallet: {str(e)}'}), 500

@wallet_bp.route('/balance/<wallet_address>', methods=['GET'])
@jwt_required()
def get_wallet_balance(wallet_address):
    """
    Get wallet balance by address
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        result = wallet_service.get_wallet_balance(wallet_address)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        logger.error(f"Get balance endpoint error: {str(e)}")
        return jsonify({'error': f'Failed to get balance: {str(e)}'}), 500

@wallet_bp.route('/list', methods=['GET'])
@jwt_required()
def list_user_wallets():
    """
    Get all wallets for the authenticated user
    
    Query Parameters:
    - include_mnemonics: true/false (default: false)
      WARNING: Setting include_mnemonics=true is EXTREMELY DANGEROUS!
      Only use for development/testing. NEVER use in production!
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        # Check if mnemonics should be included (DEVELOPMENT ONLY!)
        include_mnemonics = request.args.get('include_mnemonics', 'false').lower() == 'true'
        
        if include_mnemonics:
            logger.warning(f"SECURITY RISK: User {user_id} requested mnemonics in wallet list")
        
        result = wallet_service.get_user_wallets(user_id, include_mnemonics=include_mnemonics)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"List wallets endpoint error: {str(e)}")
        return jsonify({'error': f'Failed to list wallets: {str(e)}'}), 500

@wallet_bp.route('/transfer/prepare', methods=['POST'])
@jwt_required()
def prepare_transfer():
    """
    Prepare a transfer by creating a message for signing
    
    Request body:
    {
        "from_address": "0x...",
        "to_address": "0x...",
        "amount": 0.5,  # Amount in ETH
        "amount_usd": 1000.0  # Optional: Amount in USD
    }
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        from_address = data.get('from_address')
        to_address = data.get('to_address')
        amount = data.get('amount')
        amount_usd = data.get('amount_usd')
        
        # Validate required fields
        if not all([from_address, to_address]):
            return jsonify({'error': 'from_address and to_address are required'}), 400
        
        # Either amount or amount_usd must be provided
        if not amount and not amount_usd:
            return jsonify({'error': 'Either amount (ETH) or amount_usd is required'}), 400
        
        # If USD amount is provided, convert to ETH
        if amount_usd:
            price_result = price_service.get_eth_amount_for_usd(amount_usd)
            if not price_result['success']:
                return jsonify({'error': f'Price conversion failed: {price_result["error"]}'}), 400
            
            amount = price_result['eth_amount']
        
        # Create transfer message
        result = wallet_service.create_transfer_message(
            from_address=from_address,
            to_address=to_address,
            amount=amount,
            amount_usd=amount_usd
        )
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Prepare transfer endpoint error: {str(e)}")
        return jsonify({'error': f'Failed to prepare transfer: {str(e)}'}), 500

@wallet_bp.route('/transfer/execute', methods=['POST'])
@jwt_required()
def execute_transfer():
    """
    Execute a transfer by verifying signature and updating balances
    
    Request body:
    {
        "message": "Transfer 0.5 ETH to 0x... from 0x...",
        "signature": "0x...",
        "from_address": "0x..."
    }
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        message = data.get('message')
        signature = data.get('signature')
        from_address = data.get('from_address')
        
        # Validate required fields
        if not all([message, signature, from_address]):
            return jsonify({'error': 'message, signature, and from_address are required'}), 400
        
        # Execute transfer
        result = wallet_service.verify_and_execute_transfer(
            message=message,
            signature=signature,
            from_address=from_address
        )
        
        if result['success']:
            # Send email notification
            try:
                from models.database import User
                user = User.query.get(user_id)
                if user and user.email:
                    email_service.send_transaction_notification(
                        user.email, 
                        result['transaction']
                    )
            except Exception as e:
                logger.warning(f"Failed to send transaction email: {str(e)}")
            
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Execute transfer endpoint error: {str(e)}")
        return jsonify({'error': f'Failed to execute transfer: {str(e)}'}), 500

@wallet_bp.route('/sign-message', methods=['POST'])
@jwt_required()
def sign_message():
    """
    Sign a message with wallet private key (for frontend use)
    
    Request body:
    {
        "message": "Transfer 0.5 ETH to 0x... from 0x...",
        "wallet_address": "0x...",
        "mnemonic": "word1 word2 ... word12"
    }
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        message = data.get('message')
        wallet_address = data.get('wallet_address')
        mnemonic = data.get('mnemonic')
        
        # Validate required fields
        if not all([message, wallet_address, mnemonic]):
            return jsonify({'error': 'message, wallet_address, and mnemonic are required'}), 400
        
        # Validate mnemonic
        if not crypto_utils.validate_mnemonic(mnemonic):
            return jsonify({'error': 'Invalid mnemonic phrase'}), 400
        
        # Derive private key from mnemonic
        account_result = crypto_utils.mnemonic_to_account(mnemonic)
        if not account_result['success']:
            return jsonify({'error': account_result['error']}), 400
        
        private_key = account_result['private_key']
        address = account_result['address']
        
        # Verify wallet address matches
        if address.lower() != wallet_address.lower():
            return jsonify({'error': 'Wallet address does not match mnemonic'}), 400
        
        # Sign message
        sign_result = crypto_utils.sign_message(private_key, message)
        if not sign_result['success']:
            return jsonify({'error': sign_result['error']}), 400
        
        return jsonify({
            'success': True,
            'signature': sign_result['signature'],
            'message_hash': sign_result['message_hash'],
            'wallet_address': address
        }), 200
            
    except Exception as e:
        logger.error(f"Sign message endpoint error: {str(e)}")
        return jsonify({'error': f'Failed to sign message: {str(e)}'}), 500

@wallet_bp.route('/price/eth', methods=['GET'])
@jwt_required()
def get_eth_price():
    """
    Get current ETH price in USD
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        result = price_service.get_current_eth_price()
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Get ETH price endpoint error: {str(e)}")
        return jsonify({'error': f'Failed to get ETH price: {str(e)}'}), 500

@wallet_bp.route('/price/convert', methods=['POST'])
@jwt_required()
def convert_usd_to_eth():
    """
    Convert USD amount to ETH using Skip API
    
    Request body:
    {
        "usd_amount": 1000.0
    }
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        usd_amount = data.get('usd_amount')
        if not usd_amount:
            return jsonify({'error': 'usd_amount is required'}), 400
        
        result = price_service.get_eth_amount_for_usd(usd_amount)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Convert USD to ETH endpoint error: {str(e)}")
        return jsonify({'error': f'Failed to convert USD to ETH: {str(e)}'}), 500
