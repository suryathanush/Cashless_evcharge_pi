#!/bin/bash

# Set the path to your virtual environment
VENV_PATH="/home/surya/evcharger/env"

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Run your Python script
python3 /home/surya/evcharger/evcharger.py

# Deactivate the virtual environment
deactivate
