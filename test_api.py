#!/usr/bin/env python3
"""
Test script for CypherD Wallet Backend
BULLETPROOF testing to ensure everything works
"""

import os
import sys
import requests
import json
from datetime import datetime

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_api_endpoints():
    """Test all API endpoints"""
    base_url = "http://localhost:5001"
    
    print("🔥 Testing CypherD Wallet Backend API")
    print("=" * 50)
    
    # Test health endpoint
    print("\n1. Testing Health Endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
    
    # Test signup
    print("\n2. Testing User Signup...")
    signup_data = {
        "email": f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
        "password": "TestPassword123!",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/signup", json=signup_data)
        if response.status_code == 201:
            print("✅ Signup successful")
            user_data = response.json()
            access_token = user_data.get('access_token')
            print(f"   User ID: {user_data.get('user', {}).get('id')}")
        else:
            print(f"❌ Signup failed: {response.status_code}")
            print(f"   Error: {response.json()}")
            return
    except Exception as e:
        print(f"❌ Signup error: {str(e)}")
        return
    
    # Test signin
    print("\n3. Testing User Signin...")
    signin_data = {
        "email": signup_data["email"],
        "password": signup_data["password"]
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/signin", json=signin_data)
        if response.status_code == 200:
            print("✅ Signin successful")
            user_data = response.json()
            access_token = user_data.get('access_token')
        else:
            print(f"❌ Signin failed: {response.status_code}")
            print(f"   Error: {response.json()}")
            return
    except Exception as e:
        print(f"❌ Signin error: {str(e)}")
        return
    
    # Test wallet creation
    print("\n4. Testing Wallet Creation...")
    headers = {"Authorization": f"Bearer {access_token}"}
    wallet_data = {
        "wallet_name": "Test Wallet",
        "is_primary": True
    }
    
    try:
        response = requests.post(f"{base_url}/api/wallet/create", json=wallet_data, headers=headers)
        if response.status_code == 201:
            print("✅ Wallet creation successful")
            wallet_info = response.json()
            wallet_address = wallet_info.get('wallet', {}).get('address')
            mnemonic = wallet_info.get('mnemonic')
            print(f"   Wallet Address: {wallet_address}")
            print(f"   Starting Balance: {wallet_info.get('starting_balance')} ETH")
        else:
            print(f"❌ Wallet creation failed: {response.status_code}")
            print(f"   Error: {response.json()}")
            return
    except Exception as e:
        print(f"❌ Wallet creation error: {str(e)}")
        return
    
    # Test wallet balance
    print("\n5. Testing Wallet Balance...")
    try:
        response = requests.get(f"{base_url}/api/wallet/balance/{wallet_address}", headers=headers)
        if response.status_code == 200:
            print("✅ Balance retrieval successful")
            balance_info = response.json()
            print(f"   Balance: {balance_info.get('balance')} ETH")
        else:
            print(f"❌ Balance retrieval failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Balance retrieval error: {str(e)}")
    
    # Test ETH price
    print("\n6. Testing ETH Price...")
    try:
        response = requests.get(f"{base_url}/api/wallet/price/eth", headers=headers)
        if response.status_code == 200:
            print("✅ ETH price retrieval successful")
            price_info = response.json()
            print(f"   ETH Price: ${price_info.get('price')}")
        else:
            print(f"❌ ETH price retrieval failed: {response.status_code}")
    except Exception as e:
        print(f"❌ ETH price retrieval error: {str(e)}")
    
    # Test USD to ETH conversion
    print("\n7. Testing USD to ETH Conversion...")
    conversion_data = {"usd_amount": 1000.0}
    
    try:
        response = requests.post(f"{base_url}/api/wallet/price/convert", json=conversion_data, headers=headers)
        if response.status_code == 200:
            print("✅ USD to ETH conversion successful")
            conversion_info = response.json()
            print(f"   $1000 = {conversion_info.get('eth_amount')} ETH")
            print(f"   Rate: ${conversion_info.get('rate')}/ETH")
        else:
            print(f"❌ USD to ETH conversion failed: {response.status_code}")
            print(f"   Error: {response.json()}")
    except Exception as e:
        print(f"❌ USD to ETH conversion error: {str(e)}")
    
    print("\n🔥 API Testing Complete!")
    print("=" * 50)

if __name__ == "__main__":
    print("Starting CypherD Wallet Backend Tests...")
    print("Make sure the backend is running on http://localhost:5001")
    print("Press Ctrl+C to cancel, or Enter to continue...")
    
    try:
        input()
        test_api_endpoints()
    except KeyboardInterrupt:
        print("\nTest cancelled by user")
    except Exception as e:
        print(f"\nTest error: {str(e)}")
