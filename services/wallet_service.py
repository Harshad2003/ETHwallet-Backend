"""
Wallet service for CypherD Wallet Backend
BULLETPROOF wallet management and operations
"""

from models.database import Wallet, User, db
from utils.crypto_utils import crypto_utils
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

class WalletService:
    """Service class for wallet operations"""
    
    def __init__(self):
        self.crypto_utils = crypto_utils
    
    def create_wallet(self, user_id, wallet_name=None, is_primary=False):
        """Create a new wallet for user"""
        try:
            # Check if user exists
            user = User.query.get(user_id)
            if not user:
                return {
                    'success': False,
                    'error': 'User not found'
                }
            
            # Generate mnemonic
            mnemonic_result = self.crypto_utils.generate_mnemonic()
            if not mnemonic_result['success']:
                return mnemonic_result
            
            mnemonic = mnemonic_result['mnemonic']
            
            # Convert mnemonic to account
            account_result = self.crypto_utils.mnemonic_to_account(mnemonic)
            if not account_result['success']:
                return account_result
            
            address = account_result['address']
            
            # Encrypt mnemonic
            encrypt_result = self.crypto_utils.encrypt_mnemonic(mnemonic)
            if not encrypt_result['success']:
                return encrypt_result
            
            encrypted_mnemonic = encrypt_result['encrypted']
            
            # Generate random starting balance
            starting_balance = self.crypto_utils.generate_random_balance()
            
            # If this is primary wallet, unset other primary wallets
            if is_primary:
                Wallet.query.filter_by(user_id=user_id, is_primary=True).update({'is_primary': False})
            
            # Create wallet
            wallet = Wallet(
                user_id=user_id,
                address=address,
                mnemonic_encrypted=encrypted_mnemonic,
                balance=starting_balance,
                wallet_name=wallet_name or f"Wallet {len(user.wallets) + 1}",
                is_primary=is_primary
            )
            
            # Save to database
            db.session.add(wallet)
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Wallet created successfully',
                'wallet': wallet.to_dict(),
                'mnemonic': mnemonic,  # Only return mnemonic on creation
                'starting_balance': starting_balance
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Create wallet error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to create wallet: {str(e)}'
            }
    
    def import_wallet(self, user_id, mnemonic, wallet_name=None, is_primary=False):
        """Import existing wallet using mnemonic"""
        try:
            # Check if user exists
            user = User.query.get(user_id)
            if not user:
                return {
                    'success': False,
                    'error': 'User not found'
                }
            
            # Validate mnemonic
            if not self.crypto_utils.validate_mnemonic(mnemonic):
                return {
                    'success': False,
                    'error': 'Invalid mnemonic phrase'
                }
            
            # Convert mnemonic to account
            account_result = self.crypto_utils.mnemonic_to_account(mnemonic)
            if not account_result['success']:
                return account_result
            
            address = account_result['address']
            
            # Check if wallet already exists
            existing_wallet = Wallet.query.filter_by(address=address).first()
            if existing_wallet:
                return {
                    'success': False,
                    'error': 'Wallet with this address already exists'
                }
            
            # Encrypt mnemonic
            encrypt_result = self.crypto_utils.encrypt_mnemonic(mnemonic)
            if not encrypt_result['success']:
                return encrypt_result
            
            encrypted_mnemonic = encrypt_result['encrypted']
            
            # If this is primary wallet, unset other primary wallets
            if is_primary:
                Wallet.query.filter_by(user_id=user_id, is_primary=True).update({'is_primary': False})
            
            # Create wallet
            wallet = Wallet(
                user_id=user_id,
                address=address,
                mnemonic_encrypted=encrypted_mnemonic,
                balance=0,  # Imported wallets start with 0 balance
                wallet_name=wallet_name or f"Imported Wallet {len(user.wallets) + 1}",
                is_primary=is_primary
            )
            
            # Save to database
            db.session.add(wallet)
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Wallet imported successfully',
                'wallet': wallet.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Import wallet error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to import wallet: {str(e)}'
            }
    
    def get_wallet_balance(self, wallet_address):
        """Get wallet balance by address"""
        try:
            wallet = Wallet.query.filter_by(address=wallet_address).first()
            if not wallet:
                return {
                    'success': False,
                    'error': 'Wallet not found'
                }
            
            return {
                'success': True,
                'address': wallet.address,
                'balance': float(wallet.balance),
                'balance_eth': f"{wallet.balance:.6f} ETH"
            }
            
        except Exception as e:
            logger.error(f"Get wallet balance error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to get balance: {str(e)}'
            }
    
    def get_user_wallets(self, user_id, include_mnemonics=False):
        """Get all wallets for a user
        
        WARNING: include_mnemonics=True is EXTREMELY DANGEROUS!
        Only use for development/testing. NEVER use in production!
        """
        try:
            wallets = Wallet.query.filter_by(user_id=user_id).all()
            
            wallet_data = []
            for wallet in wallets:
                wallet_dict = wallet.to_dict()
                
                # SECURITY WARNING: Only include mnemonics if explicitly requested
                if include_mnemonics:
                    try:
                        # Decrypt mnemonic for development/testing only
                        decrypt_result = self.crypto_utils.decrypt_mnemonic(wallet.mnemonic_encrypted)
                        if decrypt_result['success']:
                            wallet_dict['mnemonic'] = decrypt_result['mnemonic']
                            logger.warning(f"SECURITY RISK: Returning mnemonic for wallet {wallet.address}")
                        else:
                            wallet_dict['mnemonic'] = "DECRYPTION_FAILED"
                            logger.error(f"Failed to decrypt mnemonic for wallet {wallet.address}")
                    except Exception as e:
                        wallet_dict['mnemonic'] = "DECRYPTION_ERROR"
                        logger.error(f"Mnemonic decryption error for wallet {wallet.address}: {str(e)}")
                
                wallet_data.append(wallet_dict)
            
            return {
                'success': True,
                'wallets': wallet_data,
                'count': len(wallets),
                'security_warning': 'Mnemonics included - DEVELOPMENT ONLY!' if include_mnemonics else None
            }
            
        except Exception as e:
            logger.error(f"Get user wallets error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to get wallets: {str(e)}'
            }
    
    def create_transfer_message(self, from_address, to_address, amount, amount_usd=None):
        """Create transfer message for signing"""
        try:
            # Validate addresses
            if not self._is_valid_address(from_address) or not self._is_valid_address(to_address):
                return {
                    'success': False,
                    'error': 'Invalid wallet address'
                }
            
            if from_address.lower() == to_address.lower():
                return {
                    'success': False,
                    'error': 'Cannot transfer to the same wallet'
                }
            
            # Validate amount (either amount or amount_usd must be provided)
            if amount is None and amount_usd is None:
                return {
                    'success': False,
                    'error': 'Either amount (ETH) or amount_usd is required'
                }
            
            if amount is not None:
                try:
                    amount_decimal = Decimal(str(amount))
                    if amount_decimal <= 0:
                        return {
                            'success': False,
                            'error': 'Amount must be greater than 0'
                        }
                except:
                    return {
                        'success': False,
                        'error': 'Invalid amount format'
                    }
            
            # Create message
            if amount_usd:
                message = f"Transfer {amount} ETH (${amount_usd:.2f} USD) to {to_address} from {from_address}"
            else:
                message = f"Transfer {amount} ETH to {to_address} from {from_address}"
            
            return {
                'success': True,
                'message': message,
                'from_address': from_address,
                'to_address': to_address,
                'amount': float(amount),
                'amount_usd': float(amount_usd) if amount_usd else None
            }
            
        except Exception as e:
            logger.error(f"Create transfer message error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to create transfer message: {str(e)}'
            }
    
    def verify_and_execute_transfer(self, message, signature, from_address):
        """Verify signature and execute transfer"""
        try:
            # Verify signature
            verify_result = self.crypto_utils.verify_signature(message, signature, from_address)
            if not verify_result['success'] or not verify_result['is_valid']:
                return {
                    'success': False,
                    'error': 'Invalid signature'
                }
            
            # Parse message to extract transfer details
            transfer_details = self._parse_transfer_message(message)
            if not transfer_details:
                return {
                    'success': False,
                    'error': 'Invalid transfer message format'
                }
            
            to_address = transfer_details['to_address']
            amount = transfer_details['amount']
            amount_usd = transfer_details.get('amount_usd')
            
            # Get sender wallet
            sender_wallet = Wallet.query.filter_by(address=from_address).first()
            if not sender_wallet:
                return {
                    'success': False,
                    'error': 'Sender wallet not found'
                }
            
            # Check balance
            if sender_wallet.balance < amount:
                return {
                    'success': False,
                    'error': 'Insufficient balance'
                }
            
            # Get or create receiver wallet
            receiver_wallet = Wallet.query.filter_by(address=to_address).first()
            if not receiver_wallet:
                # Create receiver wallet with 0 balance
                receiver_wallet = Wallet(
                    user_id=None,  # External wallet
                    address=to_address,
                    mnemonic_encrypted="",  # Empty for external wallets
                    balance=0,
                    wallet_name="External Wallet"
                )
                db.session.add(receiver_wallet)
            
            # Update balances - convert amount to Decimal for proper arithmetic
            from decimal import Decimal
            amount_decimal = Decimal(str(amount))
            sender_wallet.balance -= amount_decimal
            receiver_wallet.balance += amount_decimal
            
            # Create transaction record
            from models.database import Transaction
            transaction = Transaction(
                from_address=from_address,
                to_address=to_address,
                amount=amount,
                amount_usd=amount_usd,
                signature=signature,
                message_hash=verify_result.get('message_hash', ''),
                status='completed'
            )
            
            db.session.add(transaction)
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Transfer executed successfully',
                'transaction': transaction.to_dict(),
                'sender_balance': float(sender_wallet.balance),
                'receiver_balance': float(receiver_wallet.balance)
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Execute transfer error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to execute transfer: {str(e)}'
            }
    
    def _is_valid_address(self, address):
        """Validate Ethereum address format"""
        if not address or not isinstance(address, str):
            return False
        
        # Basic Ethereum address validation
        return address.startswith('0x') and len(address) == 42
    
    def _parse_transfer_message(self, message):
        """Parse transfer message to extract details"""
        try:
            import re
            
            # Pattern for transfer message
            pattern = r"Transfer\s+([\d.]+)\s+ETH(?:\s+\(\$([\d.]+)\s+USD\))?\s+to\s+(0x[a-fA-F0-9]{40})\s+from\s+(0x[a-fA-F0-9]{40})"
            match = re.match(pattern, message)
            
            if not match:
                return None
            
            amount = float(match.group(1))
            amount_usd = float(match.group(2)) if match.group(2) else None
            to_address = match.group(3)
            from_address = match.group(4)
            
            return {
                'amount': amount,
                'amount_usd': amount_usd,
                'to_address': to_address,
                'from_address': from_address
            }
            
        except Exception as e:
            logger.error(f"Parse transfer message error: {str(e)}")
            return None

# Global instance
wallet_service = WalletService()
