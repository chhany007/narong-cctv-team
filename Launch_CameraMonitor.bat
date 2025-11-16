@echo off
echo.
echo ========================================
echo   NARONG CCTV TEAM
echo   Camera Monitor v8
echo ========================================
echo.
echo Starting application...
echo.

cd /d "%~dp0dist"
start "" "NARONG_CCTV_TEAM.exe"

timeout /t 2 /nobreak >nul
exit
