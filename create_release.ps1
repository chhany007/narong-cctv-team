# GitHub Release Creator for Camera Monitor v8.1.0

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CREATE GITHUB RELEASE v8.1.0" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Release notes
$releaseNotes = @"
Camera Monitor v8.1.0 - Update System

What's New in v8.1.0:

NEW FEATURES:
  - Professional Windows Installer support
  - Enhanced update system (portable + installed modes)
  - Automatic data preservation during updates
  - Start Menu shortcuts and desktop icons
  - Enhanced SADP discovery performance
  - Improved NVR camera fetching
  - Better error handling for network timeouts
  - Added batch camera status checking

BUG FIXES:
  - Fixed issue with NVR login on some models
  - Resolved camera list refresh bug
  - Improved Excel sheet detection

PERFORMANCE:
  - Faster parallel camera checking
  - Reduced memory usage
  - Optimized network scans

OTHER IMPROVEMENTS:
  - Updated UI styling
  - Better logging system
  - Enhanced credential management
  - Professional installation experience

INSTALLATION OPTIONS:
  - Portable: Just run the EXE
  - Installer: Professional Windows setup with Start Menu integration
"@

# Copy to clipboard
Set-Clipboard -Value $releaseNotes
Write-Host "✓ Release notes copied to clipboard!" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  INSTRUCTIONS" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Browser will open to GitHub releases page" -ForegroundColor White
Write-Host ""
Write-Host "2. Fill in these details:" -ForegroundColor White
Write-Host "   Tag: v8.1.0" -ForegroundColor Cyan
Write-Host "   Title: Camera Monitor v8.1.0 - Update System" -ForegroundColor Cyan
Write-Host "   Description: Press Ctrl+V to paste" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Click 'Choose files' and upload:" -ForegroundColor White
Write-Host "   dist\NARONG_CCTV_TEAM.exe" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Click 'Publish release'" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

Read-Host "Press Enter to open browser"

# Open browser
$url = "https://github.com/chhany007/narong-cctv-team/releases/new?tag=v8.1.0"
Start-Process $url

Write-Host ""
Write-Host "✓ Browser opened!" -ForegroundColor Green
Write-Host ""
Write-Host "After creating the release, test the update system:" -ForegroundColor Yellow
Write-Host "  1. Run the app" -ForegroundColor White
Write-Host "  2. Click 'Check for Updates'" -ForegroundColor White
Write-Host "  3. It should show v8.1.0 is available!" -ForegroundColor White
Write-Host ""
