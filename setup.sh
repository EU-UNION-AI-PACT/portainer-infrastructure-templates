#!/bin/bash
# Quick setup script for the Portainer Template Manager

echo "🚀 Setting up Portainer Template Manager..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ pip is required but not installed."
    exit 1
fi

# Install requirements
echo "📦 Installing Python dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
else
    pip install -r requirements.txt
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p templates/individual
mkdir -p templates/merged
mkdir -p reports

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x scripts/*.py
chmod +x portainer_manager.py

# Test the installation
echo "🧪 Testing installation..."
python3 portainer_manager.py sources

echo "✅ Setup complete! You can now use the Portainer Template Manager."
echo ""
echo "Quick start commands:"
echo "  python3 portainer_manager.py update     # Full update cycle"
echo "  python3 portainer_manager.py sources    # List all sources"
echo "  python3 portainer_manager.py status     # Show current status"
echo ""
echo "For more help: python3 portainer_manager.py --help"