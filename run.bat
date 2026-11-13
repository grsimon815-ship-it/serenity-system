@echo off
title PolyglotForge Studio
echo ========================================================
echo       Launching PolyglotForge Architecture Studio
echo ========================================================
python main.py
if errorlevel 1 (
    echo.
    echo An error occurred. Make sure dependencies are installed:
    echo pip install -r requirements.txt
    pause
)
