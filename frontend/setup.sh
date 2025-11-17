#!/bin/bash

# Cerevyn Document Intelligence - Frontend Setup Script

echo "🚀 Setting up Cerevyn Document Intelligence Frontend..."
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

echo "✓ Node.js is installed: $(node --version)"
echo "✓ npm is installed: $(npm --version)"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

echo ""
echo "✅ Frontend setup complete!"
echo ""
echo "Next steps:"
echo "1. Make sure the backend is running at http://localhost:8000"
echo "2. Start the development server: npm run dev"
echo "3. Open http://localhost:3000 in your browser"
echo ""
