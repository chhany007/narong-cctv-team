@echo off
echo ========================================
echo   PUSH TO GITHUB
echo   Repository: chhany007/narong-cctv-team
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo Initializing Git repository...
git init
if errorlevel 1 (
    echo Note: Repository may already be initialized
)
echo.

echo Setting up remote...
git remote remove origin 2>nul
git remote add origin https://github.com/chhany007/narong-cctv-team.git
if errorlevel 1 (
    echo ERROR: Failed to add remote
    pause
    exit /b 1
)
echo.

echo Adding files...
git add .
if errorlevel 1 (
    echo ERROR: Failed to add files
    pause
    exit /b 1
)
echo.

echo Committing changes...
git commit -m "Initial commit - Camera Monitor v8.0.0 with auto-update system"
if errorlevel 1 (
    echo Note: Nothing to commit or commit failed
)
echo.

echo Setting default branch to main...
git branch -M main
echo.

echo ========================================
echo   READY TO PUSH
echo ========================================
echo.
echo The following files will be pushed:
echo.
git ls-files
echo.
echo ========================================
echo.
set /p CONFIRM="Push to GitHub now? (y/n): "
if /i "%CONFIRM%" NEQ "y" (
    echo Push cancelled.
    pause
    exit /b 0
)
echo.

echo Pushing to GitHub...
echo You may need to enter your GitHub credentials...
echo.
git push -u origin main
if errorlevel 1 (
    echo.
    echo ========================================
    echo   PUSH FAILED - TROUBLESHOOTING
    echo ========================================
    echo.
    echo If you see authentication errors, you need to:
    echo.
    echo Option 1: Use Personal Access Token
    echo   1. Go to: https://github.com/settings/tokens
    echo   2. Generate new token (classic)
    echo   3. Select scopes: repo (all)
    echo   4. Use token as password when prompted
    echo.
    echo Option 2: Use GitHub CLI
    echo   gh auth login
    echo.
    echo Option 3: Use SSH
    echo   Set up SSH key and use: git@github.com:chhany007/narong-cctv-team.git
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   SUCCESS!
echo ========================================
echo.
echo Files pushed to: https://github.com/chhany007/narong-cctv-team
echo.
echo NEXT STEPS:
echo.
echo 1. Build release:
echo    .\prepare_release.bat
echo.
echo 2. Create GitHub release:
echo    https://github.com/chhany007/narong-cctv-team/releases/new
echo.
echo 3. Upload exe and update version.json
echo.
echo See DEPLOY_TO_GITHUB.md for complete instructions.
echo.
pause
