#!/bin/bash
# CypherD Wallet Backend Startup Script
# BULLETPROOF startup for development

echo "🔥 Starting CypherD Wallet Backend..."
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please update .env file with your configuration!"
fi

# Create logs directory
mkdir -p logs

# Start the application
echo "🚀 Starting Flask application..."
echo "   Server will be available at: http://localhost:5001"
echo "   Press Ctrl+C to stop the server"
echo ""

python app.py
