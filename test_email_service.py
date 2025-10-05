#!/usr/bin/env python3
"""
Email Service Testing Script for CypherD Wallet Backend
BULLETPROOF email testing to verify all notifications work
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import logging
from services.email_service import email_service
from config.settings import Config

# Configure logging to see all email operations
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def test_email_configuration():
    """Test email service configuration"""
    print("🔥 TESTING EMAIL SERVICE CONFIGURATION")
    print("=" * 50)
    
    print(f"SMTP Server: {email_service.smtp_server}")
    print(f"SMTP Port: {email_service.smtp_port}")
    print(f"Username: {email_service.username}")
    print(f"Password: {'*' * len(email_service.password) if email_service.password else 'NOT SET'}")
    print(f"Use TLS: {email_service.use_tls}")
    print("=" * 50)

def test_wallet_created_email():
    """Test wallet created notification email"""
    print("\n🚀 TESTING WALLET CREATED EMAIL")
    print("=" * 50)
    
    # Mock wallet data
    wallet_data = {
        'id': 'test-wallet-id-123',
        'address': '0xC1565Bbc800D86d4F28a7C55b2C53f6c42400721',
        'balance': 9.330581999999999709,
        'wallet_name': 'Test Wallet',
        'is_primary': True,
        'created_at': '2024-01-01T12:00:00Z'
    }
    
    # Test email (replace with your email)
    test_email = "admin@sellmyshow.com"  # Using the configured email
    
    print(f"Sending wallet created email to: {test_email}")
    result = email_service.send_wallet_created_notification(test_email, wallet_data)
    
    print(f"Result: {result}")
    print("=" * 50)
    
    return result['success']

def test_transaction_email():
    """Test transaction notification email"""
    print("\n💰 TESTING TRANSACTION EMAIL")
    print("=" * 50)
    
    # Mock transaction data
    transaction_data = {
        'id': 'test-transaction-id-456',
        'from_address': '0xC1565Bbc800D86d4F28a7C55b2C53f6c42400721',
        'to_address': '0xa7ac606529AbFa32F2fBb3Dad07a925D482Ee55D',
        'amount': 0.1,
        'amount_usd': 456.27,
        'status': 'completed',
        'created_at': '2024-01-01T12:30:00Z'
    }
    
    # Test email (replace with your email)
    test_email = "admin@sellmyshow.com"  # Using the configured email
    
    print(f"Sending transaction email to: {test_email}")
    result = email_service.send_transaction_notification(test_email, transaction_data)
    
    print(f"Result: {result}")
    print("=" * 50)
    
    return result['success']

def test_email_connection():
    """Test SMTP connection without sending email"""
    print("\n🔌 TESTING SMTP CONNECTION")
    print("=" * 50)
    
    try:
        import smtplib
        
        print(f"Connecting to {email_service.smtp_server}:{email_service.smtp_port}")
        server = smtplib.SMTP(email_service.smtp_server, email_service.smtp_port)
        
        if email_service.use_tls:
            print("Starting TLS...")
            server.starttls()
        
        print("Logging in...")
        server.login(email_service.username, email_service.password)
        
        print("✅ SMTP connection successful!")
        server.quit()
        
        return True
        
    except Exception as e:
        print(f"❌ SMTP connection failed: {str(e)}")
        return False

def main():
    """Run all email tests"""
    print("🔥 CYPHERD WALLET EMAIL SERVICE TESTING")
    print("=" * 60)
    
    # Test 1: Configuration
    test_email_configuration()
    
    # Test 2: SMTP Connection
    connection_ok = test_email_connection()
    
    if not connection_ok:
        print("\n❌ SMTP CONNECTION FAILED - SKIPPING EMAIL TESTS")
        print("Check your SMTP credentials and network connection")
        return
    
    # Test 3: Wallet Created Email
    wallet_email_ok = test_wallet_created_email()
    
    # Test 4: Transaction Email
    transaction_email_ok = test_transaction_email()
    
    # Summary
    print("\n📊 EMAIL TESTING SUMMARY")
    print("=" * 50)
    print(f"SMTP Connection: {'✅ PASS' if connection_ok else '❌ FAIL'}")
    print(f"Wallet Email: {'✅ PASS' if wallet_email_ok else '❌ FAIL'}")
    print(f"Transaction Email: {'✅ PASS' if transaction_email_ok else '❌ FAIL'}")
    
    if connection_ok and wallet_email_ok and transaction_email_ok:
        print("\n🎯 ALL EMAIL TESTS PASSED! EMAIL SERVICE IS BULLETPROOF!")
    else:
        print("\n⚠️  SOME EMAIL TESTS FAILED - CHECK CONFIGURATION")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
