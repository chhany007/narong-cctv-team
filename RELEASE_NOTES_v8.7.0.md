# 🎉 NARONG CCTV Monitor v8.7.0 - Release Summary

**Release Date:** November 23, 2025  
**Developer:** Chhany  
**Team:** NARONG CCTV KOH-KONG  
**Company:** Sky-Tech

---

## 📦 What's New in v8.7.0

### 🌟 Major Features

#### 1. Professional Export System 📊
Export camera reports in multiple formats with rich styling:

- **Excel (XLSX)** - Recommended
  - Color-coded status sections (green/red/yellow)
  - Professional headers with company branding
  - Statistics boxes with visual indicators
  - Grouped by status (Online/Offline/Unknown)
  - Auto-formatted columns and print-ready

- **Word (DOCX)**
  - Professional document formatting
  - Company header and contact info
  - Formatted tables

- **PDF**
  - Styled reports with colors
  - Compact layout optimized for printing

**Export Dialog Features:**
- Company name, telephone, Telegram fields
- Logo file selection
- Settings remembered between exports

#### 2. SADP Device Discovery Tool 🔍
Complete Hikvision device discovery and management:

- **Network Scanning**
  - Scan any IP range (e.g., 192.168.0.0/16)
  - Fast parallel scanning (50+ devices at once)
  - Auto-detect cameras, NVRs, DVRs
  - Real-time progress tracking

- **Device Management**
  - View device info (IP, MAC, model, firmware, serial)
  - Configure network settings
  - Change passwords
  - Test connections
  - Export results to CSV

#### 3. Auto-Verify Offline Cameras 🔄
- Ping verification before showing offline popup
- Parallel execution for speed
- Updated status with verification results
- Shows "✅ Online (Verified)" or "🔴 Offline (Verified)"

### ✨ Improvements

#### Camera Navigation
- **Single-click** navigation from offline popup (was double-click)
- **Blue highlight** on selected items (better visibility)
- Handles duplicate IPs across NVRs correctly
- Auto-switches to "All cameras" view

#### Accurate Counting
- Fixed duplicate camera counting
- Counts ALL cameras including duplicates on different NVRs
- Display shows: Total | Unique IPs | Duplicates
- Popup count matches counter display

### 🗑️ Removed Features
- Quick Sync Workflow (replaced with SADP tool)
- Performance Dashboard (replaced with SADP tool)

---

## 📥 Installation

### Requirements
- Windows 10/11 (64-bit)
- Python 3.8+ with PyQt5

### New Dependencies
```bash
pip install python-docx reportlab
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

---

## 🚀 Quick Start

1. **Clone or update repository:**
   ```bash
   git clone https://github.com/chhany007/narong-cctv-team.git
   cd narong-cctv-team
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run application:**
   ```bash
   python NARONG_CCTV_v8.6.py
   ```

---

## 📖 Key Features Overview

### Core Functions
- 📹 **Multi-NVR Support** - Manage multiple NVR systems
- 📷 **Real-time Monitoring** - Live camera status updates
- 🔍 **Duplicate Detection** - Find duplicate cameras across sources
- 💾 **Professional Reports** - Export in Excel/Word/PDF
- 🔍 **SADP Tool** - Discover and configure Hikvision devices
- ⚡ **Auto-Verification** - Ping offline cameras automatically
- 🔐 **Secure Credentials** - Password storage with keyring

### Technical Specs
- **Platform:** Windows 10/11
- **Runtime:** Python 3.8+ with PyQt5
- **Protocols:** HTTP, RTSP, TCP, SADP
- **Database:** Excel/CSV
- **Exports:** XLSX, DOCX, PDF

---

## 📞 Support & Contact

**Developer:** Chhany  
**Telegram:** [@chhanycls](https://t.me/chhanycls)  
**Team:** NARONG CCTV KOH-KONG  
**Company:** Sky-Tech

For improvements, bug reports, or support, contact me on Telegram!

---

## 📝 Files Included

- `NARONG_CCTV_v8.6.py` - Main application
- `ivms.py` - ISAPI library for Hikvision
- `nvr_dialogs.py` - NVR management dialogs
- `requirements.txt` - Python dependencies
- `README.md` - Documentation
- `CHANGELOG.md` - Version history
- `nvr_config.json` - NVR configuration
- `sky-tech logo.png` - Application logo

---

## 🔄 Upgrade from v8.6.1

1. Pull latest changes:
   ```bash
   git pull origin main
   ```

2. Install new dependencies:
   ```bash
   pip install python-docx reportlab
   ```

3. Run application - settings will be preserved!

---

## 🎯 Next Steps

After installation:

1. **Load Excel file** with camera data
2. **Click Refresh** to check all cameras
3. **View offline popup** with verified statuses
4. **Click Export Report** to generate professional reports
5. **Use SADP Tool** to discover new devices on network

---

## ⭐ Highlights

✅ Professional export reports with rich styling  
✅ SADP tool for device discovery and management  
✅ Auto-verify offline cameras with ping  
✅ Single-click navigation with better highlighting  
✅ Accurate camera counting (handles duplicates correctly)  
✅ Clean codebase (removed 25+ unnecessary files)  
✅ Updated company branding (Sky-Tech)

---

**🌟 Professional Camera Monitoring Made Simple 🌟**
