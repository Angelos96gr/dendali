#!/bin/sh


echo "----- Setting up backend server -----"

echo "1. Activating virtual environment"
.venv/Scripts/activate

echo "2. Install dependencies"
pip install -r requirements.txt >nul

echo "3. Starting server"
python main.py