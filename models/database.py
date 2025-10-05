"""
Database models for CypherD Wallet Backend
BULLETPROOF SQLAlchemy models with proper relationships
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
import bcrypt

# Initialize SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    """User model for authentication and profile management"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with wallets
    wallets = db.relationship('Wallet', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Check password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'is_verified': self.is_verified,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Wallet(db.Model):
    """Wallet model for storing wallet information"""
    __tablename__ = 'wallets'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    address = db.Column(db.String(42), unique=True, nullable=False, index=True)
    mnemonic_encrypted = db.Column(db.Text, nullable=False)
    balance = db.Column(db.Numeric(36, 18), default=0)
    wallet_name = db.Column(db.String(100), nullable=True)
    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with transactions
    sent_transactions = db.relationship('Transaction', foreign_keys='Transaction.from_address', backref='sender_wallet', lazy=True, primaryjoin='Wallet.address == Transaction.from_address')
    received_transactions = db.relationship('Transaction', foreign_keys='Transaction.to_address', backref='receiver_wallet', lazy=True, primaryjoin='Wallet.address == Transaction.to_address')
    
    def to_dict(self):
        """Convert wallet to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'address': self.address,
            'balance': float(self.balance),
            'wallet_name': self.wallet_name,
            'is_primary': self.is_primary,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Transaction(db.Model):
    """Transaction model for storing transaction history"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    from_address = db.Column(db.String(42), nullable=False, index=True)
    to_address = db.Column(db.String(42), nullable=False, index=True)
    amount = db.Column(db.Numeric(36, 18), nullable=False)
    amount_usd = db.Column(db.Numeric(15, 2), nullable=True)
    signature = db.Column(db.Text, nullable=False)
    message_hash = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='completed')
    transaction_hash = db.Column(db.String(66), nullable=True)
    gas_fee = db.Column(db.Numeric(36, 18), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert transaction to dictionary"""
        return {
            'id': self.id,
            'from_address': self.from_address,
            'to_address': self.to_address,
            'amount': float(self.amount),
            'amount_usd': float(self.amount_usd) if self.amount_usd else None,
            'signature': self.signature,
            'message_hash': self.message_hash,
            'status': self.status,
            'transaction_hash': self.transaction_hash,
            'gas_fee': float(self.gas_fee) if self.gas_fee else None,
            'created_at': self.created_at.isoformat()
        }

class PriceCache(db.Model):
    """Price cache model for storing API price data"""
    __tablename__ = 'price_cache'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    pair = db.Column(db.String(20), nullable=False, index=True)
    price = db.Column(db.Numeric(15, 2), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert price cache to dictionary"""
        return {
            'id': self.id,
            'pair': self.pair,
            'price': float(self.price),
            'timestamp': self.timestamp.isoformat()
        }
