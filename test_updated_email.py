#!/usr/bin/env python3
"""
BULLETPROOF Email Service Test - Using Proven SellMyShow Configuration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import logging
from services.email_service import email_service

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def test_email_service():
    """Test the updated email service with proven SellMyShow configuration"""
    print("🔥 TESTING UPDATED EMAIL SERVICE")
    print("=" * 60)
    
    # Test configuration
    print(f"SMTP Server: {email_service.smtp_server}")
    print(f"SMTP Port: {email_service.smtp_port}")
    print(f"Username: {email_service.username}")
    print(f"Password: {'*' * len(email_service.password) if email_service.password else 'NOT SET'}")
    print("=" * 60)
    
    # Test wallet created email
    print("\n📧 TESTING WALLET CREATED EMAIL")
    print("-" * 40)
    
    wallet_data = {
        'id': 'test-wallet-123',
        'address': '0xC1565Bbc800D86d4F28a7C55b2C53f6c42400721',
        'balance': 9.330581999999999709,
        'wallet_name': 'My Test Wallet',
        'is_primary': True,
        'created_at': '2024-01-01T12:00:00Z'
    }
    
    # Send to the configured email
    test_email = "admin@sellmyshow.com"
    print(f"Sending wallet created email to: {test_email}")
    
    result = email_service.send_wallet_created_notification(test_email, wallet_data)
    print(f"Result: {result}")
    
    # Test transaction email
    print("\n💰 TESTING TRANSACTION EMAIL")
    print("-" * 40)
    
    transaction_data = {
        'id': 'test-transaction-456',
        'from_address': '0xC1565Bbc800D86d4F28a7C55b2C53f6c42400721',
        'to_address': '0xa7ac606529AbFa32F2fBb3Dad07a925D482Ee55D',
        'amount': 0.1,
        'amount_usd': 456.27,
        'status': 'completed',
        'created_at': '2024-01-01T12:30:00Z'
    }
    
    print(f"Sending transaction email to: {test_email}")
    result = email_service.send_transaction_notification(test_email, transaction_data)
    print(f"Result: {result}")
    
    print("\n🎯 EMAIL SERVICE TEST COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    test_email_service()
