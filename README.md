# 🎥 NARONG CCTV v8.7 - Advanced Camera Monitoring System

Professional camera monitoring and management system for NVR and IP cameras with enhanced parallel processing and duplicate detection.

![Version](https://img.shields.io/badge/version-8.6-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![License](https://img.shields.io/badge/license-Proprietary-red)

---

## ✨ Features

### 🆕 New in v8.7
- 🔍 **Advanced Duplicate Detection** - Smart duplicate camera identification across all sources
- ⚡ **Enhanced Parallel Processing** - Optimized multi-threading with configurable worker pools (6 workers by default)
- 📊 **Performance Optimization** - Improved connection timeouts and UI throttling
- 🎨 **Enhanced Visual Feedback** - Better status indicators and real-time progress tracking
- 🛠️ **Improved Error Handling** - Comprehensive logging with multiple severity levels
- 🚀 **Workflow Wizard v8.7** - Upgraded automated camera discovery process

### 🎯 Core Features
- 📹 **NVR Management** - Monitor multiple NVR systems
- 📷 **Camera Monitoring** - Real-time camera status checking
- 🔧 **SADP Discovery** - Hikvision device network discovery
- 🎦 **VLC Integration** - Direct RTSP stream viewing
- 🔐 **Credential Manager** - Secure password storage

### 🚀 Advanced Features
- ⚡ **Parallel Checking** - Fast bulk camera status verification
- 📊 **Excel Integration** - Import/export camera data
- 🌐 **Multi-Protocol** - HTTP, RTSP, TCP, SADP, Ping
- 🔄 **Auto Updates** - Built-in update system
- 📝 **Detailed Logging** - Comprehensive error tracking

---

## 📥 Download

### Latest Release: v8.0.0

**[Download NARONG_CCTV_TEAM.exe](https://github.com/chhany007/narong-cctv-team/releases/latest)**

### System Requirements
- **OS:** Windows 10/11 (64-bit)
- **RAM:** 4GB minimum
- **Storage:** 200MB
- **Network:** Internet connection for updates

---

## 🚀 Quick Start

### Installation

1. **Download** the latest release
2. **Run** `NARONG_CCTV_TEAM.exe`
3. **Load** your `ip.xlsx` file with NVR/camera data
4. **Start** monitoring!

No installation needed - it's a portable executable!

### First Use

```
1. Launch application
2. Click "📂 Load Excel" 
3. Select your ip.xlsx file
4. Click "⚡ Check All" to verify cameras
5. Double-click IP to open stream in VLC
```

---

## 📖 Documentation

- 📘 [Update System Guide](UPDATE_SYSTEM_SETUP.md)
- 📗 [User Manual](UPDATE_SYSTEM_README.md)
- 📙 [Quick Reference](UPDATE_QUICK_REFERENCE.txt)
- 📕 [Changelog](CHANGELOG.md)

---

## 🔄 Update System

### Automatic Updates
The application automatically checks for updates when started (once per day).

### Manual Check
Click the "🔄 Check for Updates" button in the toolbar anytime.

### Update Process
1. Update notification appears
2. Click "Download & Install"
3. Wait for download
4. Install automatically
5. Done!

---

## 📊 Excel File Format

Your `ip.xlsx` should have:

### NVR Sheet
```
| Name      | IP           | Subnet        | Gateway      |
|-----------|--------------|---------------|--------------|
| NVR-01    | 192.168.1.10 | 255.255.255.0 | 192.168.1.1  |
| NVR-02    | 192.168.2.10 | 255.255.255.0 | 192.168.2.1  |
```

### Camera Sheets (one per NVR)
```
Sheet: "NVR-01"
| Camera Name    | IP           |
|----------------|--------------|
| Camera-01      | 192.168.1.20 |
| Camera-02      | 192.168.1.21 |
```

---

## 🔧 Features Overview

### NVR Management
- ✅ Multiple NVR support
- ✅ Real IP detection
- ✅ Connectivity checking
- ✅ Credential storage
- ✅ Camera fetching from NVR

### Camera Monitoring
- ✅ Bulk status checking (parallel)
- ✅ Multiple check methods (SADP, TCP, Ping)
- ✅ Model detection
- ✅ Online/Offline status
- ✅ Export to CSV

### SADP Tool
- ✅ Network device discovery
- ✅ Subnet scanning
- ✅ Device information
- ✅ Batch operations

### Integration
- ✅ VLC for RTSP streams
- ✅ Web browser for HTTP
- ✅ Excel for data import/export
- ✅ Secure credential storage

---

## 🎯 Use Cases

### For IT Teams
- Monitor all cameras in building
- Quick status overview
- Bulk health checks
- Automated workflows

### For Installers
- Verify camera installations
- Check network connectivity
- Document camera information
- Export reports

### For Administrators
- Central management dashboard
- Credential management
- Quick access to camera feeds
- Historical status tracking

---

## 🔐 Security

### Credential Storage
- 🔒 Windows Keyring (if available)
- 🔒 Encrypted fallback storage
- 🔒 Auto-login support
- 🔒 Per-device credentials

### Updates
- ✅ SHA256 checksum verification
- ✅ HTTPS downloads only
- ✅ No telemetry/tracking
- ✅ User consent required

---

## 🐛 Troubleshooting

### Camera Not Detected?
- Check IP address is correct
- Verify network connectivity
- Try different check methods
- Check firewall settings

### NVR Login Failed?
- Verify credentials
- Check NVR is online
- Try default credentials
- Review logs

### Update Check Failed?
- Check internet connection
- Verify firewall allows connections
- Try manual check
- Contact administrator

---

## 📞 Support

### Documentation
- Full setup guide: `UPDATE_SYSTEM_SETUP.md`
- Quick reference: `UPDATE_QUICK_REFERENCE.txt`
- Changelog: `CHANGELOG.md`

### Logs
Check `camera_monitor.log` for detailed error information.

### Contact
For support, contact your IT administrator or open an issue on GitHub.

---

## 🛠️ Development

### Building from Source

```powershell
# Clone repository
git clone https://github.com/chhany007/narong-cctv-team.git
cd narong-cctv-team

# Install dependencies
pip install -r requirements.txt

# Run application
python CameraMonitor_Final_v7.py

# Build executable
.\build_complete.bat
```

### Requirements
- Python 3.8+
- PyQt5
- pandas
- openpyxl
- requests
- keyring (optional)

---

## 📝 Version History

### v8.0.0 (2025-11-16) - Current
- ✨ Added automatic update system
- ✨ Enhanced SADP discovery
- ✨ Improved NVR camera fetching
- ✨ Quick workflow wizard
- 🐛 Fixed NVR login issues
- 🐛 Improved error handling
- ⚡ Faster parallel checking

See [CHANGELOG.md](CHANGELOG.md) for complete history.

---

## 📜 License

Proprietary - NARONG CCTV TEAM  
All rights reserved.

---

## 🙏 Credits

**Developed by:** NARONG CCTV TEAM  
**Version:** 8.0.0  
**Last Updated:** November 16, 2025  
**Repository:** github.com/chhany007/narong-cctv-team

---

## 🔗 Links

- 🏠 [Homepage](https://github.com/chhany007/narong-cctv-team)
- 📥 [Releases](https://github.com/chhany007/narong-cctv-team/releases)
- 📖 [Documentation](https://github.com/chhany007/narong-cctv-team#readme)
- 🐛 [Issue Tracker](https://github.com/chhany007/narong-cctv-team/issues)

---

**Made with ❤️ by NARONG CCTV TEAM**
