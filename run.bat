@echo off
title Serenity System
echo Starting Serenity System...
python main.py
if errorlevel 1 (
    echo.
    echo An error occurred. Make sure dependencies are installed:
    echo pip install -r requirements.txt
    pause
)
