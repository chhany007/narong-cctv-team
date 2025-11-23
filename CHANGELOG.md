# Changelog

## Version 8.8.0 (2025-11-23)

### 🎉 Major Features

#### Enhanced Excel Export with NVR Grouping
- **Summary Sheet** with comprehensive NVR statistics
  - Overview of all NVRs with camera counts
  - Online/Offline/Unknown status breakdown per NVR
  - Uptime percentage with color-coded indicators (Green ≥90%, Orange 70-89%, Red <70%)
  - Grand total row with overall system statistics
  
- **Individual NVR Sheets** for detailed analysis
  - Separate sheet created for each NVR automatically
  - Complete camera details per NVR (Status, Name, IP, Model, Port, etc.)
  - Professional formatting with alternating row colors
  - Frozen panes for easy scrolling
  - Statistics bar showing totals per NVR

- **Smart Camera Grouping**
  - Cameras automatically grouped by NVR assignment
  - Uses `defaultdict` for efficient grouping
  - Sanitized sheet names (Excel-compatible, max 31 chars)
  - Alphabetically sorted for consistency

#### License System Enhancements
- **Fixed License Validation Algorithm**
  - Corrected signature generation to use abbreviated license types (PRO/ENT/TRI/DEM)
  - Master Key Generator and main app now use matching algorithm
  - Machine binding fully functional
  - Expiration date validation working correctly

- **Master Key Generator Complete Redesign**
  - Removed cluttered header banner and info sections
  - Modern card-based UI with clean design
  - Enhanced input fields with better focus states
  - Vertical layout for license configuration
  - Emoji icons for duration options (🔹 Trial, ⭐ 1 Year, 💎 5 Years, 🏆 10 Years)
  - License type selection with icons (💼 PROFESSIONAL, 🏢 ENTERPRISE, 🧪 TRIAL, 🎯 DEMO)
  - Larger gradient generate button (60px height)
  - Clean blue-themed result display
  - Compact action buttons with modern styling
  - Simplified window title: "🔑 License Key Generator"

#### SADP Tool Restoration
- **Fixed "Feature Removed" Error**
  - Removed duplicate stub method that was blocking access
  - Full SADP implementation now accessible via button
  - Network scanning functionality available
  - Device discovery and configuration dialogs working

### ✨ Improvements

- **Code Quality**
  - Fixed LicenseDialog initialization (2 parameters instead of 3)
  - Removed unsupported CSS properties for Qt compatibility
  - Clean, maintainable code structure
  - No syntax errors or warnings

- **User Experience**
  - Professional, modern UI design throughout
  - Consistent styling and spacing
  - Better visual hierarchy
  - Improved accessibility with cursor pointers
  - Enhanced hover states for better feedback

### 🔧 Technical Details

- **Excel Export**: Lines 5644-6022 in NARONG_CCTV_v8.6.py
- **License System**: Fixed in both NARONG_CCTV_v8.6.py and master_key_generator.py
- **SADP Tool**: Duplicate method removed at line 8465
- **Dependencies**: No new dependencies added

---

## Version 8.7.0 (2025-11-23)

### 🎉 Major Features

#### Professional Export System
- **Excel Export** with rich styling and formatting
  - Color-coded status sections (Online/Offline/Unknown)
  - Professional headers with company branding
  - Statistics boxes with visual indicators
  - Grouped data by status
  - Auto-adjusted columns and print-ready layout
  - Summary section with uptime percentage

- **Word Export** with professional formatting
  - Company header and contact information
  - Formatted tables with all camera data
  - Summary statistics section

- **PDF Export** with styled reports
  - Professional layout with headers
  - Color-coded status indicators
  - Compact tables optimized for PDF

- **Export Dialog**
  - Company name, telephone, and Telegram fields
  - Logo file selection
  - Settings saved between exports
  - Format selection (Excel/Word/PDF)

#### SADP Device Discovery Tool
- **Network Scanning** for Hikvision devices
  - Configurable IP range and timeout
  - Fast parallel scanning (50+ devices simultaneously)
  - Real-time progress tracking
  - Auto-detect cameras, NVRs, and DVRs

- **Device Management**
  - View complete device information (IP, MAC, model, firmware, serial)
  - Configure network settings (IP, gateway, subnet, port)
  - Password management interface
  - Connection testing with response time
  - Export scan results to CSV

### ✨ Improvements

#### Offline Camera Verification
- Auto-verify offline cameras with ping before showing popup
- Parallel ping execution for speed
- Updated status with verification results
- Single-click navigation from popup to table
- Blue highlight on selected items (better visibility)

#### Camera Counting System
- Fixed duplicate counting issues
- Count ALL cameras including duplicates on different NVRs
- Accurate offline camera counts
- Display: Total, Unique IPs, and Duplicates
- Popup count now matches counter display

#### Camera Location
- Enhanced camera navigation from offline popup
- Handles duplicate IPs across different NVRs correctly
- Auto-switches to "All cameras" view
- Accurate row highlighting and scrolling

### 🔧 Technical Changes

- **Removed Features**
  - Quick Sync Workflow (replaced with SADP)
  - Performance Dashboard (replaced with SADP)

- **Dependencies Added**
  - `python-docx>=0.8.11` for Word exports
  - `reportlab>=3.6.0` for PDF exports

- **Code Cleanup**
  - Removed unnecessary documentation files
  - Removed debug files and test scripts
  - Cleaned Python cache directories

### 📝 Updates

- **About Dialog**
  - Updated developer info: Chhany
  - Team: NARONG CCTV KOH-KONG
  - Company: Sky-Tech
  - Clickable Telegram contact: @chhanycls

- **Application Info**
  - Version: 8.7.0
  - Build Date: 2025-11-23
  - App ID: SkyTech.CameraMonitor.8.7.0

### 🐛 Bug Fixes

- Fixed status icon detection for verified cameras
- Fixed counter not updating after verification
- Fixed duplicate IP filtering logic
- Fixed camera location navigation issues
- Fixed datetime import in SADP export

---

## Version 8.6.1 (2025-11-22)

### Previous Features
- Smart Caching System
- Performance Dashboard
- Enhanced Error Handling
- Optimized Parallel Processing
- Advanced Metrics Tracking
