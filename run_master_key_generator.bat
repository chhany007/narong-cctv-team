@echo off
title Master Key Generator - NARONG CCTV
color 0D
cls

echo ================================================
echo   Master Key Generator - NARONG CCTV v8.8.0
echo ================================================
echo.
echo Starting application...
echo.

REM Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Run the application
python master_key_generator.py

if errorlevel 1 (
    echo.
    echo ================================================
    echo   ERROR: Failed to start application
    echo ================================================
    echo.
    echo Possible solutions:
    echo   1. Install Python 3.7 or higher
    echo   2. Install PyQt5: pip install PyQt5
    echo   3. Check for error messages above
    echo.
    pause
)
