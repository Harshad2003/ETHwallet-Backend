"""
Transaction routes for CypherD Wallet Backend
BULLETPROOF transaction history and management endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.database import Transaction, Wallet, db
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Create blueprint
transaction_bp = Blueprint('transactions', __name__)

@transaction_bp.route('/history/<wallet_address>', methods=['GET'])
@jwt_required()
def get_transaction_history(wallet_address):
    """
    Get transaction history for a wallet address
    
    Query parameters:
    - limit: Number of transactions to return (default: 50)
    - offset: Number of transactions to skip (default: 0)
    - status: Filter by transaction status (optional)
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        # Get query parameters
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        status = request.args.get('status')
        
        # Validate limit
        if limit > 100:
            limit = 100
        
        # Build query
        query = Transaction.query.filter(
            (Transaction.from_address == wallet_address) | 
            (Transaction.to_address == wallet_address)
        )
        
        # Filter by status if provided
        if status:
            query = query.filter(Transaction.status == status)
        
        # Order by creation date (newest first)
        query = query.order_by(Transaction.created_at.desc())
        
        # Get total count
        total_count = query.count()
        
        # Apply pagination
        transactions = query.offset(offset).limit(limit).all()
        
        return jsonify({
            'success': True,
            'transactions': [tx.to_dict() for tx in transactions],
            'total_count': total_count,
            'limit': limit,
            'offset': offset,
            'has_more': (offset + limit) < total_count
        }), 200
            
    except Exception as e:
        logger.error(f"Get transaction history endpoint error: {str(e)}")
        return jsonify({'error': f'Failed to get transaction history: {str(e)}'}), 500

@transaction_bp.route('/stats/<wallet_address>', methods=['GET'])
@jwt_required()
def get_transaction_stats(wallet_address):
    """
    Get transaction statistics for a wallet address
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        # Get all transactions for this wallet
        transactions = Transaction.query.filter(
            (Transaction.from_address == wallet_address) | 
            (Transaction.to_address == wallet_address)
        ).all()
        
        if not transactions:
            return jsonify({
                'success': True,
                'stats': {
                    'total_transactions': 0,
                    'total_sent': 0,
                    'total_received': 0,
                    'net_balance_change': 0,
                    'first_transaction': None,
                    'last_transaction': None
                }
            }), 200
        
        # Calculate statistics
        total_sent = sum(float(tx.amount) for tx in transactions if tx.from_address == wallet_address)
        total_received = sum(float(tx.amount) for tx in transactions if tx.to_address == wallet_address)
        net_balance_change = total_received - total_sent
        
        first_transaction = min(transactions, key=lambda x: x.created_at)
        last_transaction = max(transactions, key=lambda x: x.created_at)
        
        return jsonify({
            'success': True,
            'stats': {
                'total_transactions': len(transactions),
                'total_sent': total_sent,
                'total_received': total_received,
                'net_balance_change': net_balance_change,
                'first_transaction': first_transaction.created_at.isoformat(),
                'last_transaction': last_transaction.created_at.isoformat()
            }
        }), 200
            
    except Exception as e:
        logger.error(f"Get transaction stats endpoint error: {str(e)}")
        return jsonify({'error': f'Failed to get transaction stats: {str(e)}'}), 500

@transaction_bp.route('/<transaction_id>', methods=['GET'])
@jwt_required()
def get_transaction_details(transaction_id):
    """
    Get details of a specific transaction
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        return jsonify({
            'success': True,
            'transaction': transaction.to_dict()
        }), 200
            
    except Exception as e:
        logger.error(f"Get transaction details endpoint error: {str(e)}")
        return jsonify({'error': f'Failed to get transaction details: {str(e)}'}), 500

@transaction_bp.route('/recent', methods=['GET'])
@jwt_required()
def get_recent_transactions():
    """
    Get recent transactions across all user wallets
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        # Get user's wallet addresses
        user_wallets = Wallet.query.filter_by(user_id=user_id).all()
        wallet_addresses = [wallet.address for wallet in user_wallets]
        
        if not wallet_addresses:
            return jsonify({
                'success': True,
                'transactions': [],
                'count': 0
            }), 200
        
        # Get recent transactions
        limit = request.args.get('limit', 20, type=int)
        if limit > 50:
            limit = 50
        
        transactions = Transaction.query.filter(
            (Transaction.from_address.in_(wallet_addresses)) | 
            (Transaction.to_address.in_(wallet_addresses))
        ).order_by(Transaction.created_at.desc()).limit(limit).all()
        
        return jsonify({
            'success': True,
            'transactions': [tx.to_dict() for tx in transactions],
            'count': len(transactions)
        }), 200
            
    except Exception as e:
        logger.error(f"Get recent transactions endpoint error: {str(e)}")
        return jsonify({'error': f'Failed to get recent transactions: {str(e)}'}), 500

@transaction_bp.route('/send', methods=['POST'])
@jwt_required()
def send_transaction():
    """
    Send a transaction (alternative endpoint for direct transaction sending)
    
    Request body:
    {
        "from_address": "0x...",
        "to_address": "0x...",
        "amount": 0.5,
        "amount_usd": 1000.0,  # Optional
        "message": "Transfer 0.5 ETH to 0x... from 0x...",
        "signature": "0x..."
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
        message = data.get('message')
        signature = data.get('signature')
        
        # Validate required fields
        if not all([from_address, to_address, amount, message, signature]):
            return jsonify({'error': 'from_address, to_address, amount, message, and signature are required'}), 400
        
        # Use wallet service to execute transfer
        from services.wallet_service import wallet_service
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
                    from services.email_service import email_service
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
        logger.error(f"Send transaction endpoint error: {str(e)}")
        return jsonify({'error': f'Failed to send transaction: {str(e)}'}), 500
