"""
Crypto utilities for CypherD Wallet Backend
BULLETPROOF cryptographic operations for Web3 wallet
"""

import secrets
import hashlib
from eth_account import Account
from eth_account.messages import encode_defunct
from mnemonic import Mnemonic
from cryptography.fernet import Fernet
import base64
import logging

logger = logging.getLogger(__name__)

class CryptoUtils:
    """Utility class for cryptographic operations"""
    
    def __init__(self, encryption_key=None):
        """Initialize crypto utils with optional encryption key"""
        self.encryption_key = encryption_key or 'dev-encryption-key-32-chars'
        self.mnemonic = Mnemonic("english")
    
    def generate_mnemonic(self):
        """Generate a new 12-word mnemonic phrase"""
        try:
            mnemonic = self.mnemonic.generate(strength=128)
            return {
                'success': True,
                'mnemonic': mnemonic,
                'word_count': len(mnemonic.split())
            }
        except Exception as e:
            logger.error(f"Error generating mnemonic: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to generate mnemonic: {str(e)}'
            }
    
    def validate_mnemonic(self, mnemonic):
        """Validate a mnemonic phrase"""
        try:
            if not mnemonic or not isinstance(mnemonic, str):
                return False
            
            words = mnemonic.strip().split()
            if len(words) != 12:
                return False
            
            return self.mnemonic.check(mnemonic)
        except Exception as e:
            logger.error(f"Error validating mnemonic: {str(e)}")
            return False
    
    def mnemonic_to_account(self, mnemonic, account_index=0):
        """Convert mnemonic to private key and address"""
        try:
            if not self.validate_mnemonic(mnemonic):
                raise ValueError("Invalid mnemonic phrase")
            
            # Derive private key from mnemonic
            Account.enable_unaudited_hdwallet_features()
            account = Account.from_mnemonic(mnemonic, account_path=f"m/44'/60'/0'/0/{account_index}")
            
            return {
                'success': True,
                'private_key': account.key.hex(),
                'address': account.address,
                'account_index': account_index
            }
        except Exception as e:
            logger.error(f"Error converting mnemonic to account: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to convert mnemonic: {str(e)}'
            }
    
    def sign_message(self, private_key, message):
        """Sign a message with private key"""
        try:
            if not private_key or not message:
                raise ValueError("Private key and message are required")
            
            # Create account from private key
            account = Account.from_key(private_key)
            
            # Encode message
            message_encoded = encode_defunct(text=message)
            
            # Sign message
            signed_message = account.sign_message(message_encoded)
            
            return {
                'success': True,
                'signature': signed_message.signature.hex(),
                'message_hash': signed_message.messageHash.hex(),
                'address': account.address
            }
        except Exception as e:
            logger.error(f"Error signing message: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to sign message: {str(e)}'
            }
    
    def verify_signature(self, message, signature, address):
        """Verify a signature"""
        try:
            if not all([message, signature, address]):
                raise ValueError("Message, signature, and address are required")
            
            # Encode message
            message_encoded = encode_defunct(text=message)
            
            # Recover address from signature
            recovered_address = Account.recover_message(message_encoded, signature=signature)
            
            # Check if recovered address matches
            is_valid = recovered_address.lower() == address.lower()
            
            return {
                'success': True,
                'is_valid': is_valid,
                'recovered_address': recovered_address,
                'expected_address': address
            }
        except Exception as e:
            logger.error(f"Error verifying signature: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to verify signature: {str(e)}'
            }
    
    def encrypt_mnemonic(self, mnemonic):
        """Encrypt mnemonic for storage"""
        try:
            if not mnemonic:
                raise ValueError("Mnemonic is required")
            
            # Create Fernet cipher
            key = base64.urlsafe_b64encode(self.encryption_key.encode()[:32].ljust(32, b'0'))
            cipher = Fernet(key)
            
            # Encrypt mnemonic
            encrypted = cipher.encrypt(mnemonic.encode())
            
            return {
                'success': True,
                'encrypted': encrypted.decode()
            }
        except Exception as e:
            logger.error(f"Error encrypting mnemonic: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to encrypt mnemonic: {str(e)}'
            }
    
    def decrypt_mnemonic(self, encrypted_mnemonic):
        """Decrypt mnemonic from storage"""
        try:
            if not encrypted_mnemonic:
                raise ValueError("Encrypted mnemonic is required")
            
            # Create Fernet cipher
            key = base64.urlsafe_b64encode(self.encryption_key.encode()[:32].ljust(32, b'0'))
            cipher = Fernet(key)
            
            # Decrypt mnemonic
            decrypted = cipher.decrypt(encrypted_mnemonic.encode())
            
            return {
                'success': True,
                'mnemonic': decrypted.decode()
            }
        except Exception as e:
            logger.error(f"Error decrypting mnemonic: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to decrypt mnemonic: {str(e)}'
            }
    
    def generate_random_balance(self, min_eth=1.0, max_eth=10.0):
        """Generate random starting balance for new wallets"""
        import random
        balance = random.uniform(min_eth, max_eth)
        return round(balance, 6)  # Round to 6 decimal places
    
    def wei_to_eth(self, wei_amount):
        """Convert wei to ETH"""
        return wei_amount / (10 ** 18)
    
    def eth_to_wei(self, eth_amount):
        """Convert ETH to wei"""
        return int(eth_amount * (10 ** 18))
    
    def usdc_to_units(self, usdc_amount):
        """Convert USDC to units (6 decimals)"""
        return int(usdc_amount * (10 ** 6))
    
    def units_to_usdc(self, units):
        """Convert USDC units to USDC"""
        return units / (10 ** 6)

# Global instance
crypto_utils = CryptoUtils()
