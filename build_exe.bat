@echo off
echo ====================================
echo KKCCTV Camera Monitor - Build EXE
echo ====================================
echo.

echo Checking Python environment...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python first.
    pause
    exit /b 1
)

echo.
echo Installing/Updating required packages...
pip install --upgrade pyinstaller PyQt5 pandas openpyxl requests keyring pillow

if %errorlevel% neq 0 (
    echo ERROR: Failed to install packages!
    pause
    exit /b 1
)

echo.
echo Converting PNG logo to ICO format...
python -c "from PIL import Image; img = Image.open('sky-tech logo.png'); img.save('app_icon.ico', format='ICO', sizes=[(256,256)])"

if exist app_icon.ico (
    echo ICO file created successfully!
) else (
    echo Warning: ICO creation failed, using PNG directly
)

echo.
echo Building executable with PyInstaller...
echo This may take a few minutes...
echo.

pyinstaller --clean --noconfirm build_exe.spec

if %errorlevel% neq 0 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ====================================
echo BUILD COMPLETE!
echo ====================================
echo.
echo Executable location: dist\KKCCTV_CameraMonitor.exe
echo.
echo Features:
echo   - No console window
echo   - Logo included
echo   - All dependencies bundled
echo   - Ready to distribute
echo.
pause
