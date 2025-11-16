# GitHub Release Creator for Camera Monitor v8.2.0

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CREATE GITHUB RELEASE v8.2.0" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Release notes
$releaseNotes = @"
Camera Monitor v8.2.0 - Enhanced NVR Extraction

What's New in v8.2.0:

NEW FEATURES:
  - Enhanced NVR Camera Extraction
    * Added Hikvision ISAPI support (most reliable method)
    * Added Dahua API support for Dahua NVRs
    * Improved channel detection with IP and port info
    * Better status detection (online/offline)
    * More detailed logging for troubleshooting

  - Taskbar Icon
    * Application logo now appears in Windows taskbar
    * Better branding and easier identification

BUG FIXES:
  - Fixed update system crash on startup
  - Fixed resource path issues in bundled EXE
  - Improved NVR timeout handling

PERFORMANCE:
  - Increased NVR fetch timeout from 2s to 3s
  - Better error handling for network issues
  - More efficient camera discovery

OTHER IMPROVEMENTS:
  - Enhanced logging for NVR operations
  - Better XML parsing for Hikvision devices
  - Improved Dahua config parsing
  - Cleaner codebase
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
Write-Host "   Tag: v8.2.0" -ForegroundColor Cyan
Write-Host "   Title: Camera Monitor v8.2.0 - Enhanced NVR Extraction" -ForegroundColor Cyan
Write-Host "   Description: Press Ctrl+V to paste" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Click 'Choose files' and upload:" -ForegroundColor White
Write-Host "   dist\NARONG_CCTV_TEAM.exe (103.04 MB)" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Click 'Publish release'" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

Read-Host "Press Enter to open browser"

# Open browser
$url = "https://github.com/chhany007/narong-cctv-team/releases/new?tag=v8.2.0"
Start-Process $url

Write-Host ""
Write-Host "✓ Browser opened!" -ForegroundColor Green
Write-Host ""
Write-Host "After creating the release:" -ForegroundColor Yellow
Write-Host "  1. Users with v8.0.0 or v8.1.0 will see update notification" -ForegroundColor White
Write-Host "  2. They can download v8.2.0 automatically" -ForegroundColor White
Write-Host "  3. New features will be available immediately!" -ForegroundColor White
Write-Host ""
