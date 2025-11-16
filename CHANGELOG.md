# Changelog - NARONG CCTV TEAM Camera Monitor

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Planned Features
- Silent auto-update option for IT administrators
- Rollback to previous version
- Delta updates (smaller downloads)
- Update notifications via system tray
- Multi-language support

---

## [8.0.0] - 2025-11-16

### Added - Major Update System
- ✨ **Automatic Update System**: App now checks for updates on startup
- 🔄 **Manual Update Check**: New "Check for Updates" button in toolbar
- 📥 **One-Click Updates**: Download and install updates with single click
- 📝 **Release Notes Display**: See what's new before updating
- 🔒 **Secure Downloads**: SHA256 checksum verification
- ⏰ **Smart Checking**: Only checks once per day (not annoying)
- ❌ **Skip Version**: Option to skip unwanted updates
- 📊 **Progress Tracking**: Visual progress bar during download

### Added - Other Features
- 🚀 **Quick Workflow Wizard**: Automated setup wizard for initial configuration
- 📹 **NVR Camera Fetching**: Automatically discover cameras from NVR
- 🔧 **SADP Tool Integration**: Network discovery for Hikvision devices
- 🔄 **NVR Status Refresh**: Check all NVR connectivity with one click
- 📊 **Enhanced Logging**: Better error tracking and diagnostics

### Changed
- 🎨 Improved UI with better spacing and layout
- ⚡ Faster parallel camera checking
- 🔍 Enhanced SADP discovery with subnet targeting
- 📊 Better NVR status indicators
- 🔐 More secure credential storage

### Fixed
- 🐛 Fixed NVR login on certain models
- 🐛 Resolved camera list refresh issues
- 🐛 Improved Excel sheet detection for non-standard formats
- 🐛 Fixed timeout issues on slow networks
- 🐛 Corrected IP detection for certain NVR models

### Technical
- Added `update_manager.py` for update functionality
- Added `version_config.json` for version tracking
- Updated PyInstaller build spec to include update files
- Enhanced error handling throughout application

---

## [7.0.0] - 2025-11-01

### Added
- 📷 Camera status checking (TCP, HTTP, RTSP, Ping)
- 🗄️ NVR sidebar with overview
- 🔐 Credential manager with keyring support
- 📤 Export to CSV functionality
- 🎦 VLC integration for RTSP streams
- 🌐 Browser integration for HTTP access
- 🔍 Search and filter cameras
- 📊 Device type and model detection

### Changed
- Redesigned main interface
- Improved Excel file handling
- Better error messages

---

## Version Numbering

### Format: MAJOR.MINOR.PATCH

- **MAJOR**: Breaking changes or significant new features
  - Example: 7.0.0 → 8.0.0 (added update system)
  
- **MINOR**: New features, backwards compatible
  - Example: 8.0.0 → 8.1.0 (new feature added)
  
- **PATCH**: Bug fixes only
  - Example: 8.0.0 → 8.0.1 (bug fixed)

---

## How to Add Entries

When releasing a new version:

1. **Update Version Number** in `version_config.json`
2. **Add Entry** to this file under [Unreleased] first
3. **Move to Versioned Section** when releasing
4. **Update version.json** on server with same notes

### Categories:
- **Added**: New features
- **Changed**: Changes to existing features
- **Deprecated**: Features being removed soon
- **Removed**: Features removed
- **Fixed**: Bug fixes
- **Security**: Security improvements

### Example Entry:
```markdown
## [8.1.0] - 2025-12-01

### Added
- ✨ New camera auto-discovery feature
- 📊 Real-time bandwidth monitoring

### Fixed
- 🐛 Fixed crash when NVR offline
- 🐛 Resolved memory leak in status checker

### Changed
- ⚡ Improved startup speed by 50%
```

---

## Release Checklist

Before releasing a new version:

- [ ] Update version in `version_config.json`
- [ ] Update this CHANGELOG.md
- [ ] Build new exe: `.\build_complete.bat`
- [ ] Calculate checksum: `Get-FileHash`
- [ ] Test the exe thoroughly
- [ ] Upload exe to hosting (GitHub/Server)
- [ ] Update `version.json` on server:
  - [ ] Version number
  - [ ] Download URL
  - [ ] Checksum
  - [ ] Release notes
  - [ ] File size
  - [ ] Release date
- [ ] Test update process
- [ ] Announce to users

---

## Links

- [GitHub Repository](https://github.com/your-username/camera-monitor)
- [Issue Tracker](https://github.com/your-username/camera-monitor/issues)
- [Documentation](UPDATE_SYSTEM_SETUP.md)

---

**Note**: Dates are in YYYY-MM-DD format
