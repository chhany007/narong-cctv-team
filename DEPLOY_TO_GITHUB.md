# 🚀 Deploy to GitHub - Step by Step

Your repository: **https://github.com/chhany007/narong-cctv-team**

## ✅ Configuration Complete!

All files are already configured for your repository:
- ✅ `version_config.json` - Points to your GitHub
- ✅ `version.json` - Configured with your release URLs
- ✅ Update system ready to use!

---

## 📦 Step 1: Prepare Files for GitHub

### Files to Upload to GitHub:

```
📁 narong-cctv-team/
├── version.json                    ← MUST UPLOAD (update info)
├── README.md                       ← Recommended (project info)
├── UPDATE_SYSTEM_README.md         ← Optional (user guide)
└── releases/                       ← Created automatically by GitHub
    └── v8.1.0/
        └── NARONG_CCTV_TEAM.exe   ← Upload via GitHub Releases
```

---

## 📝 Step 2: Upload version.json to GitHub

### Option A: Via GitHub Website

```bash
1. Go to: https://github.com/chhany007/narong-cctv-team

2. Click "Add file" → "Upload files"

3. Drag and drop: version.json

4. Commit message: "Add version info for update system"

5. Click "Commit changes"
```

### Option B: Via Git Command Line

```powershell
# Navigate to your project folder
cd "d:\Coding Folder\Koh Kong Casino\IP"

# Initialize git (if not done)
git init

# Add remote
git remote add origin https://github.com/chhany007/narong-cctv-team.git

# Add version.json
git add version.json

# Commit
git commit -m "Add version info for update system"

# Push to main branch
git push -u origin main
```

---

## 🏗️ Step 3: Build Your Application

```powershell
# Make sure you're in the project folder
cd "d:\Coding Folder\Koh Kong Casino\IP"

# Build the executable
.\build_complete.bat

# Wait for build to complete...
# Result will be in: .\dist\NARONG_CCTV_TEAM.exe
```

**Build time:** ~2-3 minutes  
**Output:** `dist\NARONG_CCTV_TEAM.exe` (~103-110 MB)

---

## 🔐 Step 4: Calculate Checksum

```powershell
# Calculate SHA256 checksum
Get-FileHash -Algorithm SHA256 .\dist\NARONG_CCTV_TEAM.exe

# Output will look like:
# Algorithm       Hash
# ---------       ----
# SHA256          A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6A7B8C9D0E1F2
```

**📋 Copy this hash!** You'll need it in Step 6.

---

## 📤 Step 5: Create GitHub Release

### Via GitHub Website:

```
1. Go to: https://github.com/chhany007/narong-cctv-team/releases

2. Click "Create a new release"

3. Fill in:
   ┌─────────────────────────────────────────┐
   │ Tag version: v8.1.0                     │  ← Must match version.json
   │ Release title: v8.1.0 - Update Release  │
   │ Description: (paste release notes)      │
   └─────────────────────────────────────────┘

4. Click "Attach binaries" → Upload: NARONG_CCTV_TEAM.exe

5. Click "Publish release"

6. Copy the download URL (right-click on NARONG_CCTV_TEAM.exe → Copy link)
```

**Download URL will be:**
```
https://github.com/chhany007/narong-cctv-team/releases/download/v8.1.0/NARONG_CCTV_TEAM.exe
```

---

## 📝 Step 6: Update version.json

Edit `version.json` with your actual values:

```json
{
  "version": "8.1.0",
  "download_url": "https://github.com/chhany007/narong-cctv-team/releases/download/v8.1.0/NARONG_CCTV_TEAM.exe",
  "release_notes": "🎉 What's New in v8.1.0:\n\n✨ New Features:\n  • Automatic update system\n  • Enhanced SADP discovery\n  • Improved NVR camera fetching\n  • Better error handling\n\n🐛 Bug Fixes:\n  • Fixed NVR login issues\n  • Resolved camera refresh bugs\n  • Improved Excel detection\n\n⚡ Performance:\n  • Faster parallel checking\n  • Reduced memory usage\n  • Optimized network scans",
  "release_date": "2025-11-16",
  "file_size": 110000000,
  "checksum": "PASTE_YOUR_SHA256_HASH_HERE",
  "required": false
}
```

### What to update:
1. **checksum** ← Paste the SHA256 hash from Step 4
2. **file_size** ← Get actual size: `(Get-Item .\dist\NARONG_CCTV_TEAM.exe).Length`
3. **release_notes** ← Customize what's new
4. **download_url** ← Verify it's correct (from Step 5)

---

## 🔄 Step 7: Upload Updated version.json

### Via GitHub Website:

```
1. Go to: https://github.com/chhany007/narong-cctv-team

2. Click on "version.json" file

3. Click the pencil icon (Edit)

4. Paste your updated content

5. Commit message: "Update version info for v8.1.0 release"

6. Click "Commit changes"
```

### Via Git:

```powershell
git add version.json
git commit -m "Update version info for v8.1.0 release"
git push
```

---

## ✅ Step 8: Verify Everything Works

### Test 1: Check Raw URL

Open in browser:
```
https://raw.githubusercontent.com/chhany007/narong-cctv-team/main/version.json
```

Should show your version.json content. ✅

### Test 2: Check Download URL

Open in browser:
```
https://github.com/chhany007/narong-cctv-team/releases/download/v8.1.0/NARONG_CCTV_TEAM.exe
```

Should start downloading the exe file. ✅

### Test 3: Test Update in App

```powershell
# Lower version to trigger update
# Edit version_config.json temporarily:
"current_version": "7.0.0"

# Run the app
python CameraMonitor_Final_v7.py

# Should show update dialog! ✅

# Restore version:
"current_version": "8.0.0"
```

---

## 🎯 Quick Command Reference

```powershell
# Build
.\build_complete.bat

# Get checksum
Get-FileHash -Algorithm SHA256 .\dist\NARONG_CCTV_TEAM.exe

# Get file size
(Get-Item .\dist\NARONG_CCTV_TEAM.exe).Length

# Test app
python CameraMonitor_Final_v7.py

# Test update system
python test_update_system.py

# Upload to git
git add version.json
git commit -m "Update version info"
git push
```

---

## 📋 Release Checklist

Use this for every new release:

- [ ] **Code changes** - Make your improvements
- [ ] **Update version** in `version_config.json` (e.g., 8.0.0 → 8.1.0)
- [ ] **Build exe** - `.\build_complete.bat`
- [ ] **Get checksum** - `Get-FileHash -Algorithm SHA256`
- [ ] **Get file size** - `(Get-Item .\dist\NARONG_CCTV_TEAM.exe).Length`
- [ ] **Create GitHub release** - Upload exe with tag (e.g., v8.1.0)
- [ ] **Copy download URL** - From GitHub release
- [ ] **Update version.json** with:
  - [ ] New version number
  - [ ] Download URL
  - [ ] Checksum
  - [ ] File size
  - [ ] Release notes
  - [ ] Release date
- [ ] **Upload version.json** to GitHub
- [ ] **Test raw URL** - https://raw.githubusercontent.com/.../version.json
- [ ] **Test download** - Click exe in release
- [ ] **Test app** - Run and check for updates
- [ ] **Announce** to users!

---

## 🔥 Future Releases

### For v8.2.0 (next version):

```powershell
# 1. Make code changes
# Edit CameraMonitor_Final_v7.py

# 2. Update version
# Edit version_config.json: "current_version": "8.2.0"

# 3. Build
.\build_complete.bat

# 4. Get checksum
Get-FileHash -Algorithm SHA256 .\dist\NARONG_CCTV_TEAM.exe

# 5. Create release v8.2.0 on GitHub
# Upload NARONG_CCTV_TEAM.exe

# 6. Update version.json
{
  "version": "8.2.0",
  "download_url": "https://github.com/chhany007/narong-cctv-team/releases/download/v8.2.0/NARONG_CCTV_TEAM.exe",
  ...
}

# 7. Push to GitHub
git add version.json
git commit -m "Release v8.2.0"
git push
```

---

## 🆘 Troubleshooting

### Problem: Raw URL not accessible
**Solution:**
- Make sure repository is public
- Check version.json is in main branch
- Wait 1-2 minutes for GitHub to update

### Problem: Download fails
**Solution:**
- Verify release is published (not draft)
- Check file was uploaded to release
- Test download URL in browser

### Problem: Checksum mismatch
**Solution:**
- Recalculate checksum: `Get-FileHash`
- Update version.json with correct hash
- Push updated version.json

### Problem: App doesn't check for updates
**Solution:**
- Verify `update_check_url` in version_config.json
- Check internet connection
- Look at camera_monitor.log for errors
- Try manual check: Click "Check for Updates" button

---

## 📞 Your Repository URLs

**Repository:** https://github.com/chhany007/narong-cctv-team  
**Releases:** https://github.com/chhany007/narong-cctv-team/releases  
**Version File (Raw):** https://raw.githubusercontent.com/chhany007/narong-cctv-team/main/version.json  
**Download URL Pattern:** https://github.com/chhany007/narong-cctv-team/releases/download/v{VERSION}/NARONG_CCTV_TEAM.exe

---

## 🎉 You're Ready!

Your update system is configured for:
- ✅ Repository: chhany007/narong-cctv-team
- ✅ Automatic update checks
- ✅ GitHub Releases hosting
- ✅ Secure downloads with checksums

**Follow the steps above to deploy your first release!**

---

**Last Updated:** November 16, 2025  
**Repository:** github.com/chhany007/narong-cctv-team  
**Version:** 8.0.0
