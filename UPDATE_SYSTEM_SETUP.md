# 🔄 Update System Setup Guide

## Overview
Your Camera Monitor application now includes an automatic update system that checks for new versions and allows users to download and install updates with a single click.

## 📋 How It Works

### User Experience:
1. **Automatic Check**: App checks for updates on startup (once per day)
2. **Update Dialog**: If update available, shows version info and release notes
3. **One-Click Update**: User clicks "Download & Install" button
4. **Auto Install**: Update downloads, installer launches, app closes
5. **Done**: New version installed automatically

### Features:
- ✅ Automatic update checking on startup
- ✅ Manual "Check for Updates" button
- ✅ Beautiful update dialog with release notes
- ✅ Progress bar during download
- ✅ Checksum verification for security
- ✅ Skip version option
- ✅ Respects update check frequency (max once per day)

## 🚀 Setup Instructions

### Option 1: GitHub Releases (Recommended)

#### 1. Create GitHub Repository
```bash
# Create a new repository on GitHub
# Example: github.com/your-username/camera-monitor-releases
```

#### 2. Upload version.json
Upload `version.json` to your repository with this structure:
```json
{
  "version": "8.1.0",
  "download_url": "https://github.com/USERNAME/REPO/releases/download/v8.1.0/NARONG_CCTV_TEAM.exe",
  "release_notes": "What's new in this version...",
  "release_date": "2025-11-20",
  "file_size": 108000000,
  "checksum": "sha256_hash_of_exe",
  "required": false
}
```

#### 3. Configure Update URL
Edit `version_config.json`:
```json
{
  "current_version": "8.0.0",
  "app_name": "NARONG CCTV TEAM - Camera Monitor",
  "update_check_url": "https://raw.githubusercontent.com/USERNAME/REPO/main/version.json",
  "check_on_startup": true,
  "auto_download": false
}
```

#### 4. Create Release
When you build a new version:
```bash
# 1. Build the new exe
.\build_complete.bat

# 2. Calculate checksum
Get-FileHash -Algorithm SHA256 .\dist\NARONG_CCTV_TEAM.exe

# 3. Create GitHub release
#    - Go to: github.com/USERNAME/REPO/releases/new
#    - Tag: v8.1.0
#    - Upload: NARONG_CCTV_TEAM.exe
#    - Get download URL

# 4. Update version.json with:
#    - New version number
#    - New download URL
#    - New checksum
#    - Release notes

# 5. Commit and push version.json
```

### Option 2: Your Own Web Server

#### 1. Setup Web Server
You need:
- Web server with HTTPS (required for downloads)
- Public URL accessible to users
- Space for exe files (~100MB per version)

#### 2. Create Directory Structure
```
your-server.com/
  └── updates/
      ├── version.json
      ├── v8.0.0/
      │   └── NARONG_CCTV_TEAM.exe
      └── v8.1.0/
          └── NARONG_CCTV_TEAM.exe
```

#### 3. Configure Update URL
Edit `version_config.json`:
```json
{
  "update_check_url": "https://your-server.com/updates/version.json"
}
```

#### 4. Upload Files
```bash
# Upload version.json
# Upload exe to versioned folder
# Update version.json with download URL
```

### Option 3: Cloud Storage (Dropbox, Google Drive, etc.)

#### 1. Upload Files
- Upload `version.json` to cloud storage
- Upload exe files
- Get public sharing links

#### 2. Configure URLs
```json
{
  "update_check_url": "https://dl.dropboxusercontent.com/...../version.json",
}
```

**Note**: Some cloud providers may throttle or block direct downloads. GitHub Releases is more reliable.

## 📝 Updating version.json

When releasing a new version, update `version.json`:

```json
{
  "version": "8.2.0",  // ← New version number
  "download_url": "https://..../NARONG_CCTV_TEAM.exe",  // ← New download URL
  "release_notes": "✨ New features:\n  • Feature 1\n  • Feature 2",  // ← What's new
  "release_date": "2025-12-01",  // ← Release date
  "file_size": 110000000,  // ← File size in bytes
  "checksum": "abc123...",  // ← SHA256 checksum
  "required": false  // ← Set to true to force update
}
```

### Calculate Checksum
```powershell
# PowerShell
Get-FileHash -Algorithm SHA256 .\dist\NARONG_CCTV_TEAM.exe
```

Output:
```
Algorithm       Hash
---------       ----
SHA256          A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6A7B8C9D0E1F2
```

Copy the hash to `checksum` field in version.json.

## 🔧 Configuration Options

### version_config.json

```json
{
  "current_version": "8.0.0",           // Current app version
  "app_name": "Camera Monitor",          // App name
  "update_check_url": "https://...",    // URL to version.json
  "check_on_startup": true,             // Check on app start
  "auto_download": false                // Auto-download (future feature)
}
```

### Update Check Behavior

- **Startup Check**: Once per day maximum
- **Manual Check**: Anytime user clicks button
- **Skip Version**: User can skip specific version
- **Required Update**: Set `"required": true` to force update

## 🎨 Customization

### Change Update Check Frequency

Edit `update_manager.py`, line ~80:
```python
# Check at most once per day
if time.time() - last_check < 86400:  # ← Change 86400 (1 day) to your preference
    return False
```

### Disable Automatic Checks

Edit `version_config.json`:
```json
{
  "check_on_startup": false  // ← Disable auto-check
}
```

### Customize Update Dialog

Edit `update_manager.py`, class `UpdateDialog` to change:
- Colors
- Button text
- Dialog size
- Styling

## 📦 Build Process

### 1. Update Version Number
Edit `version_config.json`:
```json
{
  "current_version": "8.1.0"  // ← Increment version
}
```

### 2. Build EXE
```bash
.\build_complete.bat
```

### 3. Calculate Checksum
```powershell
Get-FileHash -Algorithm SHA256 .\dist\NARONG_CCTV_TEAM.exe
```

### 4. Upload to Server
- Upload exe to hosting service
- Get download URL

### 5. Update version.json
```json
{
  "version": "8.1.0",
  "download_url": "https://.../NARONG_CCTV_TEAM.exe",
  "checksum": "actual_sha256_hash",
  ...
}
```

### 6. Commit and Push
```bash
git add version.json
git commit -m "Release v8.1.0"
git push
```

## 🧪 Testing

### Test Update Check
1. Lower version in `version_config.json` to "7.0.0"
2. Run app: `python CameraMonitor_Final_v7.py`
3. Should show update dialog
4. Test download and install

### Test Manual Check
1. Click "Check for Updates" button
2. Should check immediately (ignores frequency limit)

### Test Skip Version
1. Click "Skip This Version"
2. Restart app
3. Should not show update for skipped version

## 🔒 Security

### Checksum Verification
- Always provide SHA256 checksum
- App verifies download integrity
- Prevents corrupted/tampered files

### HTTPS Required
- Use HTTPS URLs for downloads
- Prevents man-in-the-middle attacks

### Code Signing (Optional)
For production deployment:
```bash
# Sign exe with certificate
signtool sign /f certificate.pfx /p password /t http://timestamp.server .\dist\NARONG_CCTV_TEAM.exe
```

## 🐛 Troubleshooting

### Update Check Fails
**Problem**: "Could not connect to update server"
**Solution**: 
- Check internet connection
- Verify update_check_url is accessible
- Check firewall settings

### Download Fails
**Problem**: "Download failed: Connection timeout"
**Solution**:
- Check file is publicly accessible
- Verify download_url is correct
- Test URL in browser

### Checksum Mismatch
**Problem**: "Checksum verification failed"
**Solution**:
- Recalculate checksum
- Update version.json
- Re-upload file if corrupted

### Update Button Missing
**Problem**: No "Check for Updates" button
**Solution**:
- Ensure `update_manager.py` is in same folder
- Check console for import errors
- Rebuild with: `.\build_complete.bat`

## 📱 User Instructions

### How Users Update

1. **Automatic Notification**
   - Update dialog appears on startup
   - Shows new version and features
   
2. **Manual Check**
   - Click "🔄 Check for Updates" button
   - See if update available

3. **Download & Install**
   - Click "📥 Download & Install"
   - Wait for download (progress bar shown)
   - Click "🚀 Install Now"
   - App closes, installer starts

4. **Options**
   - "⏰ Remind Me Later": Check again later
   - "❌ Skip This Version": Don't show this version again

## 📊 Release Workflow

```
┌─────────────────────┐
│  1. Code Changes    │
│  Edit Python code   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  2. Update Version  │
│  version_config.json│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  3. Build EXE       │
│  build_complete.bat │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  4. Calculate Hash  │
│  Get-FileHash       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  5. Upload EXE      │
│  GitHub/Server      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  6. Update JSON     │
│  version.json       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  7. Test Update     │
│  Install & verify   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  8. Distribute      │
│  Users get update   │
└─────────────────────┘
```

## 🎯 Quick Start Checklist

- [ ] Create GitHub repository for releases
- [ ] Upload version.json to repository
- [ ] Get raw URL for version.json
- [ ] Update version_config.json with URL
- [ ] Build new exe: `.\build_complete.bat`
- [ ] Calculate checksum: `Get-FileHash`
- [ ] Create GitHub release with exe
- [ ] Update version.json with download URL and checksum
- [ ] Test update system
- [ ] Distribute to users

## 📚 Additional Resources

- GitHub Releases: https://docs.github.com/en/repositories/releasing-projects-on-github
- PyInstaller: https://pyinstaller.org/
- Code Signing: https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool

---

**Need Help?**
- Check logs in `camera_monitor.log`
- Review error messages in update dialog
- Test URLs in browser
- Verify file permissions

**Version**: 1.0  
**Last Updated**: November 2025
