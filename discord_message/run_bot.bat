@echo off
@echo "Installing requirements, please wait..."
pip install -r resources\requirements.txt
cls
@echo "Starting script."
python pyfiles\bot.py

