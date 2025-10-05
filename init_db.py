#!/usr/bin/env python3
"""
Database initialization script for CypherD Wallet Backend
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from models.database import User, Wallet, Transaction, PriceCache

def init_database():
    """Initialize the database with tables"""
    print("🔥 Initializing CypherD Wallet Database...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Test database connection
            user_count = User.query.count()
            print(f"✅ Database connection working! User count: {user_count}")
            
            return True
            
        except Exception as e:
            print(f"❌ Database initialization failed: {str(e)}")
            return False

if __name__ == "__main__":
    success = init_database()
    if success:
        print("🔥 Database initialization complete!")
    else:
        print("❌ Database initialization failed!")
        sys.exit(1)
