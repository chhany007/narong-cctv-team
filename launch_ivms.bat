@echo off
REM IVMS NVR Control - GUI Launcher
REM Professional camera management system

echo ========================================
echo   IVMS NVR Control System - GUI
echo ========================================
echo.

REM Check if virtual environment exists
if exist ".venv\Scripts\python.exe" (
    echo Using virtual environment...
    .venv\Scripts\python.exe IVMS\ivms_gui.py
) else if exist "D:\Coding Folder\Koh Kong Casino\.venv\Scripts\python.exe" (
    echo Using project virtual environment...
    "D:\Coding Folder\Koh Kong Casino\.venv\Scripts\python.exe" IVMS\ivms_gui.py
) else (
    echo Using system Python...
    python IVMS\ivms_gui.py
)

if errorlevel 1 (
    echo.
    echo Error: Failed to launch IVMS GUI
    echo.
    echo Make sure you have installed the requirements:
    echo   pip install -r IVMS\requirements.txt
    echo.
    pause
)
