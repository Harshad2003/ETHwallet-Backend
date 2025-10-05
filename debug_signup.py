#!/usr/bin/env python3
"""
Debug script for CypherD Wallet Backend
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from models.database import User
from services.auth_service import auth_service

def test_signup():
    """Test user signup functionality"""
    print("🔥 Testing User Signup...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Test signup
            result = auth_service.signup(
                email="test@example.com",
                password="TestPassword123!",
                first_name="Test",
                last_name="User"
            )
            
            print(f"Signup result: {result}")
            
            if result['success']:
                print("✅ Signup successful!")
                print(f"User ID: {result['user']['id']}")
                print(f"Email: {result['user']['email']}")
            else:
                print(f"❌ Signup failed: {result['error']}")
                
        except Exception as e:
            print(f"❌ Signup error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_signup()
