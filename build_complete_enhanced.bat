@echo off
echo ========================================
echo   COMPLETE BUILD SYSTEM
echo   NARONG CCTV TEAM - Camera Monitor
echo ========================================
echo.
echo This will create:
echo   1. Portable EXE (standalone)
echo   2. Windows Installer (professional setup)
echo.
pause

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

REM Check PyInstaller
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo.
echo ========================================
echo   STEP 1: Building Portable EXE
echo ========================================
echo.

REM Clean previous build
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build with PyInstaller
echo Building standalone executable...
pyinstaller --clean --noconfirm build_complete.spec

if not exist "dist\NARONG_CCTV_TEAM.exe" (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ✅ Portable EXE created: dist\NARONG_CCTV_TEAM.exe
echo.

REM Calculate checksums and sizes
echo ========================================
echo   PORTABLE VERSION INFO
echo ========================================
echo.
powershell -Command "Get-FileHash -Algorithm SHA256 '.\dist\NARONG_CCTV_TEAM.exe' | Format-List"
powershell -Command "$size = (Get-Item '.\dist\NARONG_CCTV_TEAM.exe').Length; Write-Host 'File Size:' $size 'bytes' '(' ([math]::Round($size/1MB, 2)) 'MB)'"
echo.

echo ========================================
echo   STEP 2: Creating Windows Installer
echo ========================================
echo.

REM Check for Inno Setup
set INNO_SETUP="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist %INNO_SETUP% (
    set INNO_SETUP="C:\Program Files\Inno Setup 6\ISCC.exe"
)

if not exist %INNO_SETUP% (
    echo.
    echo ⚠️  Inno Setup not found!
    echo.
    echo To create Windows Installer, install Inno Setup:
    echo   https://jrsoftware.org/isdl.php
    echo.
    echo For now, you can use the portable version:
    echo   dist\NARONG_CCTV_TEAM.exe
    echo.
    goto :skip_installer
)

echo Building Windows Installer...
%INNO_SETUP% installer_script.iss

if exist "installer_output\NARONG_CCTV_Team_Setup_v8.1.0.exe" (
    echo.
    echo ✅ Installer created: installer_output\NARONG_CCTV_Team_Setup_v8.1.0.exe
    echo.
    
    echo ========================================
    echo   INSTALLER VERSION INFO
    echo ========================================
    echo.
    powershell -Command "Get-FileHash -Algorithm SHA256 '.\installer_output\NARONG_CCTV_Team_Setup_v8.1.0.exe' | Format-List"
    powershell -Command "$size = (Get-Item '.\installer_output\NARONG_CCTV_Team_Setup_v8.1.0.exe').Length; Write-Host 'File Size:' $size 'bytes' '(' ([math]::Round($size/1MB, 2)) 'MB)'"
    echo.
) else (
    echo ⚠️  Installer build failed
)

:skip_installer

echo.
echo ========================================
echo   BUILD COMPLETE!
echo ========================================
echo.
echo 📦 Created Files:
echo.
echo   PORTABLE:
if exist "dist\NARONG_CCTV_TEAM.exe" (
    echo   ✅ dist\NARONG_CCTV_TEAM.exe
)
echo.
echo   INSTALLER:
if exist "installer_output\NARONG_CCTV_Team_Setup_v8.1.0.exe" (
    echo   ✅ installer_output\NARONG_CCTV_Team_Setup_v8.1.0.exe
) else (
    echo   ⚠️  Not created (Inno Setup required)
)
echo.
echo ========================================
echo   NEXT STEPS
echo ========================================
echo.
echo 1. Test both versions locally
echo.
echo 2. Create GitHub Release:
echo    https://github.com/chhany007/narong-cctv-team/releases/new
echo.
echo 3. Upload BOTH files:
echo    - NARONG_CCTV_TEAM.exe (portable)
echo    - NARONG_CCTV_Team_Setup_v8.1.0.exe (installer)
echo.
echo 4. Update version.json with BOTH URLs:
echo    {
echo      "download_url": "...NARONG_CCTV_TEAM.exe",
echo      "installer_url": "...Setup_v8.1.0.exe",
echo      ...
echo    }
echo.
echo 5. Copy checksums above to version.json
echo.
echo 6. Push to GitHub
echo.
echo ========================================
echo.

pause
