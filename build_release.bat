@echo off
echo ========================================
echo Building NARONG CCTV v8.8.0 Executable
echo ========================================
echo.

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install/upgrade PyInstaller
echo.
echo Installing PyInstaller...
python -m pip install --upgrade pyinstaller

REM Clean previous builds
echo.
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "NARONG_CCTV_v8.8.0.exe" del "NARONG_CCTV_v8.8.0.exe"

REM Build executable
echo.
echo Building executable...
pyinstaller --clean build_v8.8.0.spec

REM Check if build successful
if exist "dist\NARONG_CCTV_v8.8.0.exe" (
    echo.
    echo ========================================
    echo Build Successful!
    echo ========================================
    echo.
    echo Executable location: dist\NARONG_CCTV_v8.8.0.exe
    echo Size: 
    dir "dist\NARONG_CCTV_v8.8.0.exe" | find "NARONG_CCTV_v8.8.0.exe"
    echo.
    
    REM Copy to root directory
    copy "dist\NARONG_CCTV_v8.8.0.exe" .
    echo.
    echo Executable copied to: %CD%\NARONG_CCTV_v8.8.0.exe
    echo.
    echo ========================================
    echo Ready for Release!
    echo ========================================
) else (
    echo.
    echo ========================================
    echo Build Failed!
    echo ========================================
    echo Check the output above for errors.
)

echo.
pause
