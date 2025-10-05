"""
CypherD Wallet Backend - SQLite Version
A bulletproof Flask backend for Web3 wallet operations
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
import logging
from datetime import datetime

# Import database
from models.database import db

# Initialize extensions
jwt = JWTManager()

def create_app(config_name=None):
    """Application factory pattern - BULLETPROOF setup"""
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(f'config.settings.{config_name.title()}Config')
    
    # Initialize extensions
    jwt.init_app(app)
    db.init_app(app)
    # CORS hardcoded to allow all origins (development only)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, app.config['LOG_LEVEL']),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.wallet_routes import wallet_bp
    from routes.transaction_routes import transaction_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(wallet_bp, url_prefix='/api/wallet')
    app.register_blueprint(transaction_bp, url_prefix='/api/transactions')
    
    # Initialize database tables
    with app.app_context():
        db.create_all()
        print("🔥 Database tables created/verified!")
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return {
            'status': 'healthy', 
            'message': 'CypherD Wallet API is running!',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        }
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🔥 CypherD Wallet API Starting...")
    print("🚀 Server running on http://localhost:5001")
    print("📋 Available endpoints:")
    print("   GET  /api/health - Health check")
    print("   POST /api/auth/signup - User registration")
    print("   POST /api/auth/signin - User login")
    print("   GET  /api/auth/profile - Get user profile")
    print("   PUT  /api/auth/profile - Update user profile")
    print("   POST /api/auth/refresh - Refresh token")
    print("   POST /api/wallet/create - Create new wallet")
    print("   POST /api/wallet/import - Import existing wallet")
    print("   GET  /api/wallet/balance/<address> - Get wallet balance")
    print("   GET  /api/wallet/list - List user wallets")
    print("   POST /api/wallet/transfer/prepare - Prepare transfer")
    print("   POST /api/wallet/transfer/execute - Execute transfer")
    print("   POST /api/wallet/sign-message - Sign message")
    print("   GET  /api/wallet/price/eth - Get ETH price")
    print("   POST /api/wallet/price/convert - Convert USD to ETH")
    print("   GET  /api/transactions/history/<address> - Get transaction history")
    print("   GET  /api/transactions/stats/<address> - Get transaction stats")
    print("🔥 STAY HARD! API is ready to DOMINATE!")
    app.run(debug=True, host='0.0.0.0', port=5001)
