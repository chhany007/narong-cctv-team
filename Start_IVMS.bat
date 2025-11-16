@echo off
REM IVMS NVR Control - Complete Standalone Application
REM Launch script for Windows

echo.
echo ================================================
echo   IVMS NVR Control System
echo   Professional Camera Management
echo ================================================
echo.

REM Check for Python virtual environment
if exist ".venv\Scripts\python.exe" (
    echo Starting IVMS with virtual environment...
    .venv\Scripts\python.exe IVMS_Complete.py
) else (
    echo Starting IVMS with system Python...
    python IVMS_Complete.py
)

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start IVMS
    echo.
    echo Requirements:
    echo   - Python 3.7+
    echo   - PyQt5
    echo   - requests
    echo   - keyring (optional)
    echo.
    echo Install with: pip install PyQt5 requests keyring
    echo.
    pause
)
