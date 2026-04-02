#!/bin/bash

# Influencer Data Processor Setup Script

echo "--- Setting up Influencer Data Processor ---"

# 1. Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# 2. Upgrade pip and install dependencies
echo "Installing dependencies (pandas, openpyxl, gspread, google-auth)..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install pandas openpyxl gspread google-auth

echo ""
echo "Setup complete!"
echo "To run the processor, use: ./run.sh"
