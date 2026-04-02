#!/bin/bash

# Influencer Data Processor Execution Script

# Ensure we are in the script directory
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

echo "Starting Influencer Data Processor..."
./venv/bin/python3 process_influencers.py
