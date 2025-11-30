#!/bin/bash

# Multi-Agent System Setup Script

set -e

echo "=================================="
echo "Multi-Agent System Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Check if Ollama is installed
echo ""
echo "Checking Ollama installation..."
if command -v ollama &> /dev/null; then
    echo "✓ Ollama is installed"
    
    # Check if Ollama is running
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "✓ Ollama is running"
    else
        echo "⚠ Ollama is not running. Starting Ollama..."
        echo "Please run 'ollama serve' in another terminal"
    fi
else
    echo "✗ Ollama is not installed"
    echo "Please install Ollama from: https://ollama.ai"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists"
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
echo ""
if [ -f ".env" ]; then
    echo ".env file already exists"
else
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo "⚠ Please review and update .env with your settings"
fi

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p data/chroma data/workspace data/cache logs

# Check available Ollama models
echo ""
echo "Checking available Ollama models..."
ollama list

# Offer to pull recommended models
echo ""
echo "Would you like to pull recommended models? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "Pulling llama3.1:8b..."
    ollama pull llama3.1:8b
    
    echo "Pulling codellama:13b..."
    ollama pull codellama:13b
    
    echo "✓ Models downloaded"
fi

# Run a simple test
echo ""
echo "Running simple test..."
python examples/simple_agent.py

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Review and update .env file"
echo "2. Run examples: python examples/research_pipeline.py"
echo "3. Launch Streamlit UI: streamlit run streamlit_app/app.py"
echo ""
echo "Documentation:"
echo "- Setup Guide: docs/SETUP.md"
echo "- Architecture: docs/ARCHITECTURE.md"
echo "- Custom Agents: docs/CUSTOM_AGENTS.md"
echo ""
