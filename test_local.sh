#!/bin/bash
# Test script for local backend verification before deployment

echo "🧪 Testing Water Quality Backend Locally"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if we're in the right directory
if [ ! -f "api.py" ]; then
    echo "❌ Error: api.py not found. Please run this script from the backend-render directory."
    exit 1
fi

echo "📦 Installing dependencies..."
pip3 install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

echo "🚀 Starting Flask server on http://localhost:5000"
echo "   Press Ctrl+C to stop the server"
echo ""
echo "📡 Available endpoints:"
echo "   - http://localhost:5000/api/latest"
echo "   - http://localhost:5000/api/historical"
echo "   - http://localhost:5000/api/alerts"
echo ""
echo "💡 Tip: Open another terminal and run:"
echo "   curl http://localhost:5000/api/latest"
echo ""
echo "========================================"
echo ""

# Run the Flask app
python3 api.py

