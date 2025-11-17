#!/bin/bash

# Cerevyn Document Intelligence - Backend Setup Script

echo "🚀 Setting up Cerevyn Document Intelligence Backend..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✓ Python is installed: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please add your GROQ_API_KEY to the .env file"
else
    echo "✓ .env file already exists"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads
mkdir -p chroma_db

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "Next steps:"
echo "1. Add your Groq API key to the .env file"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Start the server: python main.py"
echo ""
