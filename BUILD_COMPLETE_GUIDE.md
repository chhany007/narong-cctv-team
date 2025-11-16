# 🚀 Complete Build & Deploy Guide

## 🎯 Overview

You now have a **professional-grade update system** that supports:
- ✅ **Portable EXE** - Single file, run anywhere
- ✅ **Windows Installer** - Professional setup with Start Menu integration
- ✅ **Automatic Updates** - Users update with one click
- ✅ **Data Preservation** - All user data kept during updates
- ✅ **Dual-Mode Support** - Portable and installed modes work seamlessly

---

## 📦 Build Both Versions

### Quick Build (Recommended):
```powershell
.\build_complete_enhanced.bat
```

This creates:
1. **Portable**: `dist\NARONG_CCTV_TEAM.exe`
2. **Installer**: `installer_output\NARONG_CCTV_Team_Setup_v8.1.0.exe`

---

## 🛠️ Prerequisites

### Required:
- ✅ Python 3.8+ (you have this)
- ✅ PyInstaller (auto-installs if missing)

### Optional (for installer):
- 📦 **Inno Setup 6**
  - Download: https://jrsoftware.org/isdl.php
  - Install to default location
  - Enables professional Windows installer creation

**Without Inno Setup:** You can still create the portable version!

---

## 📝 Step-by-Step Deployment

### Step 1: Build Both Versions

```powershell
cd "d:\Coding Folder\Koh Kong Casino\IP"
.\build_complete_enhanced.bat
```

**Output:**
```
✅ dist\NARONG_CCTV_TEAM.exe (portable)
✅ installer_output\NARONG_CCTV_Team_Setup_v8.1.0.exe (installer)
```

**Copy the checksums shown!** You'll need them.

### Step 2: Test Locally

**Test Portable:**
```powershell
.\dist\NARONG_CCTV_TEAM.exe
```

**Test Installer:**
```powershell
.\installer_output\NARONG_CCTV_Team_Setup_v8.1.0.exe
```

Verify:
- ✅ App launches
- ✅ All features work
- ✅ Update button appears

### Step 3: Create GitHub Release

1. Go to: https://github.com/chhany007/narong-cctv-team/releases
2. Click **"Create a new release"**
3. Fill in:
   - **Tag**: `v8.1.0`
   - **Title**: `v8.1.0 - Professional Installer & Enhanced Updates`
   - **Description**:
     ```markdown
     ## 🎉 What's New in v8.1.0
     
     ### ✨ Major Improvements
     - Professional Windows Installer
     - Enhanced update system
     - Automatic data preservation
     - Start Menu integration
     
     ### 📦 Installation Options
     
     **Portable Version** (Recommended for first-time users):
     - Download: NARONG_CCTV_TEAM.exe
     - No installation needed
     - Just run and go!
     
     **Installer Version** (Recommended for permanent installation):
     - Download: NARONG_CCTV_Team_Setup_v8.1.0.exe
     - Professional Windows installation
     - Start Menu shortcuts
     - Easy uninstall
     
     Both versions support automatic updates!
     
     ### 🐛 Bug Fixes
     - Fixed NVR login issues
     - Improved camera detection
     - Better error handling
     
     ### ⚡ Performance
     - Faster camera checking
     - Reduced memory usage
     - Optimized network operations
     ```

4. **Upload both files**:
   - Drag `NARONG_CCTV_TEAM.exe`
   - Drag `NARONG_CCTV_Team_Setup_v8.1.0.exe`

5. Click **"Publish release"**

6. **Copy download URLs** (right-click each file → Copy link address):
   - Portable: `https://github.com/chhany007/narong-cctv-team/releases/download/v8.1.0/NARONG_CCTV_TEAM.exe`
   - Installer: `https://github.com/chhany007/narong-cctv-team/releases/download/v8.1.0/NARONG_CCTV_Team_Setup_v8.1.0.exe`

### Step 4: Update version.json

Edit `version.json` with real values:

```json
{
  "version": "8.1.0",
  "download_url": "https://github.com/chhany007/narong-cctv-team/releases/download/v8.1.0/NARONG_CCTV_TEAM.exe",
  "installer_url": "https://github.com/chhany007/narong-cctv-team/releases/download/v8.1.0/NARONG_CCTV_Team_Setup_v8.1.0.exe",
  "release_notes": "...",
  "release_date": "2025-11-20",
  "file_size": 110000000,
  "installer_size": 115000000,
  "checksum": "PASTE_PORTABLE_SHA256_HERE",
  "installer_checksum": "PASTE_INSTALLER_SHA256_HERE",
  "required": false,
  "portable": true
}
```

**What to update:**
- ✅ `checksum` - Portable EXE SHA256 (from Step 1)
- ✅ `installer_checksum` - Installer SHA256 (from Step 1)
- ✅ `file_size` - Portable EXE size in bytes
- ✅ `installer_size` - Installer size in bytes
- ✅ `download_url` - From Step 3
- ✅ `installer_url` - From Step 3

### Step 5: Push to GitHub

```powershell
git add version.json
git commit -m "Release v8.1.0 - Professional installer and enhanced updates"
git push
```

### Step 6: Verify Everything

**Test update check URL:**
```
https://raw.githubusercontent.com/chhany007/narong-cctv-team/main/version.json
```
Should show your JSON content ✅

**Test downloads:**
- Click portable link → Should download
- Click installer link → Should download

**Test in app:**
1. Edit `version_config.json`: `"current_version": "7.0.0"`
2. Run app
3. Should show update dialog with BOTH options
4. Test download
5. Restore: `"current_version": "8.0.0"`

---

## 🎯 How Users Get Updates

### Portable Users:
1. App checks for updates
2. Shows dialog: "Update available"
3. Clicks "Download & Install"
4. Downloads new **NARONG_CCTV_TEAM.exe**
5. Replaces old one
6. **Data preserved** ✅

### Installed Users:
1. App checks for updates
2. Shows dialog: "Update available"
3. Clicks "Download & Install"
4. Downloads **installer**
5. Runs installer silently
6. Updates program files
7. **User data in AppData preserved** ✅

---

## 📁 File Locations

### Portable Mode:
```
Your Folder\
├── NARONG_CCTV_TEAM.exe        ← App
├── ip.xlsx                      ← Your data
├── camera_monitor.log           ← Your logs
├── check_history.json           ← Your history
└── creds_*.json                 ← Your credentials
```

### Installed Mode:
```
C:\Program Files\NARONG CCTV Team\
├── NARONG_CCTV_TEAM.exe        ← App (updated)
├── ip.xlsx                      ← Shared data
└── README.md                    ← Docs

C:\Users\USERNAME\AppData\Roaming\NARONG CCTV Team\
├── camera_monitor.log           ← User logs
├── check_history.json           ← User history
└── creds_*.json                 ← User credentials
```

**User data always preserved!** ✅

---

## 🔄 Future Updates Workflow

For v8.2.0, v8.3.0, etc:

```powershell
# 1. Make code changes
# Edit CameraMonitor_Final_v7.py

# 2. Update version in version_config.json
"current_version": "8.2.0"

# 3. Update installer_script.iss
#define MyAppVersion "8.2.0"

# 4. Build both versions
.\build_complete_enhanced.bat

# 5. Create GitHub release with BOTH files

# 6. Update version.json with BOTH URLs and checksums

# 7. Push
git add version.json
git commit -m "Release v8.2.0"
git push

# Done! Users get update notification automatically
```

---

## ✨ Benefits

### For Users:
- ✅ **Choice**: Portable or installed
- ✅ **Easy**: One-click updates
- ✅ **Safe**: Data always preserved
- ✅ **Professional**: Real Windows installer
- ✅ **Convenient**: Start Menu shortcuts

### For You:
- ✅ **Flexible**: Two deployment options
- ✅ **Easy**: One build script for both
- ✅ **Professional**: Industry-standard Inno Setup
- ✅ **Smart**: Automatic mode detection
- ✅ **Trackable**: Version info in registry

---

## 🆘 Troubleshooting

### Inno Setup Not Found?
- Install from: https://jrsoftware.org/isdl.php
- Or skip installer (portable still works!)

### Build Fails?
```powershell
# Clean and rebuild
rmdir /s /q build dist
pip install --upgrade pyinstaller
.\build_complete_enhanced.bat
```

### Installer Doesn't Work?
- Check Inno Setup version (need 6.x)
- Verify all files exist in paths
- Check installer_script.iss for typos

### Update Not Detected?
- Verify version.json is accessible
- Check checksums match
- Ensure URLs are correct
- Test in browser first

---

## 📊 Comparison

| Feature | Portable | Installer |
|---------|----------|-----------|
| Installation | None | Yes |
| Start Menu | No | Yes |
| Desktop Icon | No | Optional |
| Uninstaller | No | Yes |
| Registry Entry | No | Yes |
| Updates | Yes ✅ | Yes ✅ |
| Data Preserved | Yes ✅ | Yes ✅ |
| Admin Required | No | Yes |
| File Size | Smaller | Slightly larger |

**Recommendation:** Offer both! Let users choose.

---

## 🎉 You're Ready!

Your complete build system is ready:
- ✅ Portable EXE build
- ✅ Windows Installer build
- ✅ Automatic update system
- ✅ Data preservation
- ✅ Professional deployment

**Run this to build everything:**
```powershell
.\build_complete_enhanced.bat
```

**Then follow the deployment steps above!**

---

**Build Date:** November 16, 2025  
**Version:** 8.1.0  
**Repository:** github.com/chhany007/narong-cctv-team  
**Status:** Production Ready! 🚀
