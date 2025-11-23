# GitHub Release Upload Guide

## Upload NARONG CCTV v8.8.0 to GitHub Releases

### Step 1: Go to GitHub Releases
1. Open browser: https://github.com/chhany007/narong-cctv-team/releases
2. Click **"Draft a new release"** button

### Step 2: Fill Release Information
- **Tag:** Select existing tag `v8.8.0`
- **Release Title:** `NARONG CCTV v8.8.0 - Excel NVR Grouping & License Fixes`
- **Description:** Copy content from `RELEASE_NOTES_v8.8.0.md`

### Step 3: Upload Executable
1. Click **"Attach binaries by dropping them here or selecting them"**
2. Select file: `NARONG_CCTV_v8.8.0.exe` (114 MB)
3. Wait for upload to complete

### Step 4: Optional Additional Files
You can also upload:
- `RELEASE_NOTES_v8.8.0.md` - Release notes

### ⚠️ DO NOT UPLOAD (Admin Only Files):
- ❌ `master_key_generator.py` - **KEEP PRIVATE** (admin license control)
- ❌ `run_master_key_generator.bat` - **KEEP PRIVATE**
- ❌ `MASTER_KEY_GENERATOR_README.md` - **KEEP PRIVATE**
- These files are for admin use only to generate license keys

### Step 5: Publish Release
1. Check **"Set as the latest release"**
2. Click **"Publish release"** button
3. ✅ Done! Release is now live

---

## Quick Copy-Paste for Release Description

```markdown
# NARONG CCTV v8.8.0

**Major Features:**
- 📊 Excel Export with NVR Grouping (summary + individual sheets)
- 🔑 Fixed License Validation Algorithm (signature mismatch resolved)
- 🎨 Master Key Generator Redesign (modern, cleaner UI)
- 🛠️ SADP Tool Fully Restored (removed duplicate stub)

**Download:**
- `NARONG_CCTV_v8.8.0.exe` (114 MB) - Main application executable

**Full release notes:** See `RELEASE_NOTES_v8.8.0.md` for complete details.

**Requirements:** Windows 10/11, 4GB RAM, 200MB disk space

**License Activation:** Use included Master Key Generator to create license keys.
```

---

## Files Ready for Upload

Located in: `D:\Coding Folder\Koh Kong Casino\IP\`

### ✅ Public Release Files (Upload to GitHub):
- **NARONG_CCTV_v8.8.0.exe** (114 MB) - Main executable
- **RELEASE_NOTES_v8.8.0.md** - Full release notes (optional)

### ❌ Admin Only Files (DO NOT Upload):
- **master_key_generator.py** - License generator (KEEP PRIVATE)
- **run_master_key_generator.bat** - Generator launcher (KEEP PRIVATE)
- **MASTER_KEY_GENERATOR_README.md** - Generator docs (KEEP PRIVATE)

**Important:** Only you (admin) should have the Master Key Generator to control license distribution.

---

## Alternative: Using GitHub CLI (if installed)

If you install GitHub CLI later, you can upload with:

```powershell
# PUBLIC RELEASE - DO NOT include master_key_generator files
gh release create v8.8.0 `
  --title "NARONG CCTV v8.8.0 - Excel NVR Grouping & License Fixes" `
  --notes-file "RELEASE_NOTES_v8.8.0.md" `
  "NARONG_CCTV_v8.8.0.exe#Main Application Executable"
```

**Note:** Master Key Generator files are intentionally excluded (admin use only).

---

**Release URL after publishing:**  
`https://github.com/chhany007/narong-cctv-team/releases/tag/v8.8.0`
