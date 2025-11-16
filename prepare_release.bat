@echo off
echo ========================================
echo   FIRST RELEASE HELPER
echo   Repository: chhany007/narong-cctv-team
echo ========================================
echo.

echo Step 1: Building executable...
echo.
call build_complete.bat
if errorlevel 1 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)
echo.

echo Step 2: Calculating checksum...
echo.
powershell -Command "Get-FileHash -Algorithm SHA256 '.\dist\NARONG_CCTV_TEAM.exe' | Format-List"
echo.

echo Step 3: Getting file size...
echo.
powershell -Command "$size = (Get-Item '.\dist\NARONG_CCTV_TEAM.exe').Length; Write-Host 'File Size:' $size 'bytes' '(' ([math]::Round($size/1MB, 2)) 'MB)'"
echo.

echo ========================================
echo   NEXT STEPS:
echo ========================================
echo.
echo 1. Go to: https://github.com/chhany007/narong-cctv-team/releases
echo.
echo 2. Click "Create a new release"
echo.
echo 3. Tag version: v8.1.0
echo    Release title: v8.1.0 - Update Release
echo.
echo 4. Upload: dist\NARONG_CCTV_TEAM.exe
echo.
echo 5. Copy the checksum above and update version.json:
echo    - Set "checksum" to the SHA256 hash
echo    - Set "file_size" to the bytes shown above
echo    - Set "download_url" to the release download link
echo.
echo 6. Upload version.json to GitHub:
echo    - Via website: Add file -^> Upload files
echo    - Or via git: git add version.json ^&^& git commit -m "Update" ^&^& git push
echo.
echo 7. Test by opening:
echo    https://raw.githubusercontent.com/chhany007/narong-cctv-team/main/version.json
echo.
echo 8. Test update in app:
echo    - Edit version_config.json: "current_version": "7.0.0"
echo    - Run: python CameraMonitor_Final_v7.py
echo    - Should show update dialog!
echo.
echo ========================================
echo   Files ready in: .\dist\
echo ========================================
echo.

pause
