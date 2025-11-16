@echo off
echo ====================================
echo NARONG CCTV TEAM - Build Complete EXE
echo ====================================
echo.

echo Checking Python environment...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
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
echo Cleaning old build...
if exist build rmdir /s /q build
if exist dist\NARONG_CCTV_TEAM.exe del /q dist\NARONG_CCTV_TEAM.exe

echo.
echo Building COMPLETE standalone executable...
echo This includes: Logo, IP.XLSX, and all dependencies
echo Please wait (this may take 3-5 minutes)...
echo.

pyinstaller --clean --noconfirm build_complete.spec

if %errorlevel% neq 0 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo Cleaning temporary files...
if exist build rmdir /s /q build
if exist app_icon.ico del /q app_icon.ico
if exist __pycache__ rmdir /s /q __pycache__

echo.
echo ====================================
echo BUILD COMPLETE!
echo ====================================
echo.
echo Executable: dist\NARONG_CCTV_TEAM.exe
echo.
echo Features:
echo   - Software renamed to NARONG CCTV TEAM
echo   - No console window
echo   - Logo embedded
echo   - IP.XLSX embedded (no external file needed)
echo   - All dependencies included
echo   - 100%% standalone - ready to run anywhere
echo.
pause
