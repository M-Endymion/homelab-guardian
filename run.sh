#!/bin/bash
# Homelab Guardian - Quick Start Script

echo "🚀 Starting Homelab Guardian..."

# Check if dependencies are installed
if ! command -v streamlit &> /dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo "🌐 Opening dashboard..."
streamlit run app.py --server.headless true
