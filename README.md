Try the live mock Web3 wallet: https://ethwallet-app.vercel.app/
# ETHwallet Flask Backend - SQLite Version

This is a clean, modular, and production-ready backend for a mock Web3 wallet application. Built with Flask, JWT authentication, SQLite database, and comprehensive crypto utilities.

## 🚀 Features

- **User Authentication**: JWT-based auth with secure password hashing
- **Wallet Management**: Create, import, and manage multiple wallets
- **Transaction Processing**: Secure transfer operations with signature verification
- **Price Integration**: Real-time ETH/USD conversion using Skip API
- **Email Notifications**: Transaction and wallet creation notifications
- **Crypto Operations**: Mnemonic generation, signing, and validation
- **Modular Architecture**: Clean separation of concerns with services and routes

## 🛠 Tech Stack

- **Backend**: Flask 2.3.3
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT with Flask-JWT-Extended
- **Crypto**: eth-account, mnemonic, cryptography
- **Email**: SMTP with HTML templates
- **API Integration**: Skip API for price conversion

## 📁 Project Structure

```
backend_sqlite/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── env.example           # Environment configuration template
├── config/
│   ├── __init__.py
│   └── settings.py       # Configuration classes
├── models/
│   ├── __init__.py
│   └── database.py       # SQLAlchemy models
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py    # Authentication endpoints
│   ├── wallet_routes.py  # Wallet management endpoints
│   └── transaction_routes.py # Transaction endpoints
├── services/
│   ├── __init__.py
│   ├── auth_service.py   # Authentication business logic
│   ├── wallet_service.py # Wallet operations
│   ├── price_service.py  # Price fetching and conversion
│   └── email_service.py  # Email notifications
└── utils/
    ├── __init__.py
    └── crypto_utils.py   # Cryptographic utilities
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Navigate to the backend directory
cd backend_sqlite

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env file with your configuration
# At minimum, update:
# - SECRET_KEY
# - JWT_SECRET_KEY
# - ENCRYPTION_KEY
# - SMTP credentials (for email notifications)
```

### 3. Run the Application

```bash
# Run the Flask app
python app.py
```

The API will be available at `http://localhost:5001`

## 📋 API Endpoints

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User login
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile
- `POST /api/auth/change-password` - Change password
- `POST /api/auth/refresh` - Refresh access token

### Wallet Management
- `POST /api/wallet/create` - Create new wallet
- `POST /api/wallet/import` - Import existing wallet
- `GET /api/wallet/balance/<address>` - Get wallet balance
- `GET /api/wallet/list` - List user wallets
- `POST /api/wallet/transfer/prepare` - Prepare transfer
- `POST /api/wallet/transfer/execute` - Execute transfer
- `POST /api/wallet/sign-message` - Sign message
- `GET /api/wallet/price/eth` - Get ETH price
- `POST /api/wallet/price/convert` - Convert USD to ETH

### Transactions
- `GET /api/transactions/history/<address>` - Get transaction history
- `GET /api/transactions/stats/<address>` - Get transaction stats
- `GET /api/transactions/<id>` - Get transaction details
- `GET /api/transactions/recent` - Get recent transactions
- `POST /api/transactions/send` - Send transaction

### Health Check
- `GET /api/health` - API health status

## 🔐 Security Features

- **Password Hashing**: bcrypt for secure password storage
- **JWT Authentication**: Secure token-based authentication
- **Mnemonic Encryption**: Fernet encryption for wallet mnemonics
- **Signature Verification**: Cryptographic signature validation
- **Input Validation**: Comprehensive request validation
- **CORS Protection**: Configurable cross-origin resource sharing

## 💰 Wallet Operations

### Creating a Wallet

```bash
curl -X POST http://localhost:5001/api/wallet/create \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "wallet_name": "My First Wallet",
    "is_primary": true
  }'
```

### Importing a Wallet

```bash
curl -X POST http://localhost:5001/api/wallet/import \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "mnemonic": "word1 word2 word3 ... word12",
    "wallet_name": "Imported Wallet"
  }'
```

### Preparing a Transfer

```bash
curl -X POST http://localhost:5001/api/wallet/transfer/prepare \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "from_address": "0x...",
    "to_address": "0x...",
    "amount": 0.5
  }'
```

### Executing a Transfer

```bash
curl -X POST http://localhost:5001/api/wallet/transfer/execute \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Transfer 0.5 ETH to 0x... from 0x...",
    "signature": "0x...",
    "from_address": "0x..."
  }'
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `development` |
| `SECRET_KEY` | Flask secret key | Required |
| `JWT_SECRET_KEY` | JWT secret key | Required |
| `DATABASE_URL` | Database connection string | `sqlite:///cypherd_wallet.db` |
| `ENCRYPTION_KEY` | Encryption key for mnemonics | Required |
| `SMTP_USERNAME` | Email username | Optional |
| `SMTP_PASSWORD` | Email password | Optional |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |

### Database Models

- **User**: User accounts with authentication
- **Wallet**: Wallet addresses and encrypted mnemonics
- **Transaction**: Transaction history and details
- **PriceCache**: Cached price data for performance


