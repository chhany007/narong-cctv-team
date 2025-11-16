# 🔄 Camera Monitor - Automatic Update System

Your Camera Monitor application now includes an **automatic update system** that keeps your software up-to-date with the latest features and bug fixes!

## ✨ What's New

### For Users:
- ✅ **Automatic Update Checks**: App checks for updates when you start it (once per day)
- ✅ **One-Click Updates**: Download and install updates with a single click
- ✅ **Update Notifications**: See what's new in each version with release notes
- ✅ **Manual Check**: Click "🔄 Check for Updates" button anytime
- ✅ **Smart Updates**: Skip versions you don't want, or install later

### For Administrators:
- ✅ **Easy Deployment**: Upload new version, update one JSON file, done!
- ✅ **Secure Downloads**: SHA256 checksum verification
- ✅ **GitHub Integration**: Use GitHub Releases for hosting (free!)
- ✅ **Flexible Hosting**: Works with any web server or cloud storage

## 🚀 How It Works

### User Experience

1. **Startup Check** (Automatic)
   - App checks for updates when started
   - Only checks once per day (not annoying!)
   
2. **Update Available Dialog**
   ```
   ┌────────────────────────────────────┐
   │  🔔 Update Available!              │
   │                                    │
   │  Current Version: 8.0.0            │
   │  New Version: 8.1.0 ✨             │
   │                                    │
   │  What's New:                       │
   │  • Enhanced SADP discovery         │
   │  • Improved NVR camera fetching    │
   │  • Better error handling           │
   │                                    │
   │  [📥 Download & Install]           │
   │  [⏰ Remind Me Later]              │
   │  [❌ Skip This Version]            │
   └────────────────────────────────────┘
   ```

3. **Download Progress**
   ```
   Downloading update... 45%
   [███████████░░░░░░░░░░░░░]
   ```

4. **Install**
   - Installer launches automatically
   - App closes
   - New version installs
   - Done! 🎉

### Manual Check

Click the "🔄 Check for Updates" button in the toolbar anytime to check for updates.

## 📁 Files Added

```
d:\Coding Folder\Koh Kong Casino\IP\
├── update_manager.py           ← Update system logic
├── version_config.json         ← Version configuration
├── version.json               ← Sample version info (for server)
├── UPDATE_SYSTEM_SETUP.md     ← Complete setup guide
└── UPDATE_SYSTEM_README.md    ← This file
```

## 🔧 For Users

### How to Update

1. **Automatic Way** (Recommended)
   - Just start the app
   - If update available, dialog appears
   - Click "Download & Install"
   - Wait for download
   - Click "Install Now"
   - Done!

2. **Manual Way**
   - Click "🔄 Check for Updates" button
   - Follow same steps as above

### Options

- **Remind Me Later**: Check again next time you start the app
- **Skip This Version**: Don't show me this version again (but show newer ones)

### Troubleshooting

**Update check fails?**
- Check internet connection
- Try manual check: Click "🔄 Check for Updates"
- Contact your administrator

**Download fails?**
- Check internet connection
- Check available disk space (need ~100MB)
- Try again later

## 🔧 For Administrators

### Quick Setup (GitHub Releases - Free!)

1. **Create GitHub Repository**
   ```
   github.com/your-username/camera-monitor-releases
   ```

2. **Upload version.json**
   - Copy `version.json` to repository
   - Get raw URL: `https://raw.githubusercontent.com/USERNAME/REPO/main/version.json`

3. **Edit version_config.json**
   ```json
   {
     "update_check_url": "https://raw.githubusercontent.com/USERNAME/REPO/main/version.json"
   }
   ```

4. **Build and Deploy**
   ```powershell
   # Build new version
   .\build_complete.bat
   
   # Calculate checksum
   Get-FileHash -Algorithm SHA256 .\dist\NARONG_CCTV_TEAM.exe
   
   # Create GitHub release
   # - Upload exe file
   # - Get download URL
   
   # Update version.json with:
   # - New version number
   # - Download URL
   # - Checksum
   # - Release notes
   ```

### Release Workflow

```
Code Changes → Update Version → Build EXE → Upload → Update JSON → Users Get Update
```

See **UPDATE_SYSTEM_SETUP.md** for complete instructions!

## 📊 Version Information

### Current Version: 8.0.0

**Features:**
- NVR management
- Camera monitoring  
- SADP device discovery
- VLC integration
- Credential management
- Automatic updates! (New!)

### Version Format

Versions follow **Semantic Versioning**: `MAJOR.MINOR.PATCH`

- **MAJOR**: Big changes, may break compatibility (e.g., 8.0.0 → 9.0.0)
- **MINOR**: New features, backwards compatible (e.g., 8.0.0 → 8.1.0)  
- **PATCH**: Bug fixes (e.g., 8.1.0 → 8.1.1)

## 🔒 Security

### Safe Updates
- ✅ Downloads verified with SHA256 checksum
- ✅ HTTPS required for downloads
- ✅ No auto-install without user permission
- ✅ Can skip unwanted updates

### Privacy
- ✅ Only checks version number (no personal data sent)
- ✅ No tracking or analytics
- ✅ Update check is optional (can be disabled)

## ⚙️ Configuration

### Disable Automatic Checks

Edit `version_config.json`:
```json
{
  "check_on_startup": false
}
```

Users can still manually check with the button.

### Change Check Frequency

Default: Once per day  
To change: Edit `update_manager.py` (see setup guide)

## 📞 Support

**For Users:**
- Contact your IT administrator
- Check camera_monitor.log for errors

**For Administrators:**
- See UPDATE_SYSTEM_SETUP.md for full documentation
- Check version.json is accessible from user computers
- Verify download URLs are correct

## 🎯 Benefits

### For Users
- ✅ Always have latest features
- ✅ Bug fixes delivered automatically
- ✅ No manual download/install needed
- ✅ See what's new before updating

### For IT Teams
- ✅ Easy deployment (one JSON file)
- ✅ Centralized version control
- ✅ No need to manually update each computer
- ✅ Users update themselves!

## 📝 What's Next?

Future improvements planned:
- Silent auto-update option (for IT)
- Rollback to previous version
- Delta updates (smaller downloads)
- Update notifications via system tray

---

## 🆘 Quick Help

### Users

**How do I update?**
→ Click "Download & Install" when dialog appears

**Can I update later?**
→ Yes! Click "Remind Me Later"

**I don't want this version**
→ Click "Skip This Version"

### Administrators

**How do I release an update?**
→ See UPDATE_SYSTEM_SETUP.md

**Where do I host files?**
→ GitHub Releases (free) or your own server

**How do I configure update URL?**
→ Edit version_config.json

---

**Software**: NARONG CCTV TEAM - Camera Monitor  
**Version**: 8.0.0  
**Update System**: v1.0  
**Last Updated**: November 2025

For complete setup instructions, see: **UPDATE_SYSTEM_SETUP.md**
