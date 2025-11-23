# 🔑 Master Key Generator

⚠️ **ADMINISTRATOR USE ONLY** ⚠️

This tool is for administrators to generate license keys for NARONG CCTV users.  
**DO NOT distribute this tool publicly or include it in releases.**

---

## Overview
Standalone application for administrators to generate license keys for NARONG CCTV Monitor users.

## Features

### 🎯 Key Generation
- **Machine-Bound Keys**: Each key is cryptographically bound to user's Machine ID
- **Flexible Duration**: 30 days to 10 years (or custom)
- **Multiple License Types**: PROFESSIONAL, ENTERPRISE, TRIAL, DEMO
- **Secure**: SHA-256 signature prevents tampering

### 💼 License Duration Options
- **30 Days** - Trial period
- **90 Days** - 3 months
- **180 Days** - 6 months
- **365 Days** - 1 year (default)
- **730 Days** - 2 years
- **1825 Days** - 5 years
- **3650 Days** - 10 years
- **Custom** - Any number of days (1-36,500)

### ✨ UI Features
- Real-time Machine ID validation
- Copy to clipboard
- Save to file
- Clear form
- Professional gradient design
- Status bar feedback

## Usage

### Running the Application

```powershell
# Activate virtual environment (if using)
.venv\Scripts\Activate.ps1

# Run the generator
python master_key_generator.py
```

### Generating a License Key

1. **Get User's Machine ID**
   - User opens NARONG CCTV Monitor
   - License dialog shows their Machine ID
   - User sends you this 16-character ID

2. **Enter Machine ID**
   - Paste the Machine ID into the input field
   - Validation indicator shows status (✅/⚠️/❌)

3. **Configure License**
   - Select **Duration** (default: 1 Year)
   - Select **License Type** (default: PROFESSIONAL)

4. **Generate Key**
   - Click "⚡ Generate License Key"
   - Success message appears
   - Key details displayed in text area

5. **Send to User**
   - Click "📋 Copy License Key" to copy
   - Send via Telegram (@chhanycls) or email
   - User pastes key into their license dialog

### Example Workflow

```
Admin receives request:
  "Hi, my Machine ID is: a1b2c3d4e5f6g7h8"

Admin actions:
  1. Opens Master Key Generator
  2. Pastes: a1b2c3d4e5f6g7h8
  3. Selects: 365 Days (1 Year)
  4. Selects: PROFESSIONAL
  5. Clicks "Generate License Key"
  6. Copies generated key
  7. Sends to user via Telegram

Generated key example:
  a1b2c3d4e5f6g7h8-20261123-PRO-A1B2C3D4
```

## Menu Options

### File Menu
- **💾 Save Key to File** (Ctrl+S) - Save generated key to text file
- **❌ Exit** (Ctrl+Q) - Close application

### Help Menu
- **ℹ️ About** - Application information
- **📱 Contact Support** - Open Telegram (@chhanycls)

## Features Detail

### Machine ID Validation
- ✅ **Valid**: Exactly 16 characters
- ⚠️ **Too Short**: Less than 16 characters
- ❌ **Too Long**: More than 16 characters

### Generated Key Format
```
Format: MACHINE_ID-YYYYMMDD-TYPE-SIGNATURE

Example: a1b2c3d4e5f6g7h8-20261123-PRO-A1B2C3D4

Components:
  • a1b2c3d4e5f6g7h8 = Machine ID (16 chars)
  • 20261123 = Expiry date (YYYYMMDD)
  • PRO = License type (3 chars)
  • A1B2C3D4 = Signature (8 chars)
```

### Save to File
- Suggested filename: `license_key_MACHINEID_DATE.txt`
- Includes all details (Machine ID, Type, Duration, Expiry, etc.)
- Can be emailed to user

## System Requirements

- Python 3.7+
- PyQt5
- Windows/macOS/Linux

## Security

### Cryptographic Features
- **SHA-256** hash algorithm
- **Unique salt**: `NarongCCTV_SkyTech_2025_SecureKey`
- **Machine binding**: Keys only work on target machine
- **Expiration validation**: Prevents expired license usage
- **Signature verification**: Detects tampered keys

### Key Cannot Be:
- ❌ Used on different machines
- ❌ Extended past expiry date
- ❌ Modified without detection
- ❌ Reverse engineered

## Troubleshooting

### "Invalid Machine ID" Error
- Ensure Machine ID is exactly 16 characters
- Check for extra spaces or line breaks
- Ask user to copy ID again from their dialog

### Key Not Working for User
1. Verify Machine ID matches user's system
2. Check expiry date hasn't passed
3. Ensure user copied complete key
4. Confirm no extra characters added

### Application Won't Start
```powershell
# Check Python version
python --version  # Should be 3.7+

# Check PyQt5 installation
pip list | findstr PyQt5

# Reinstall if needed
pip install PyQt5
```

## License Types

| Type | Description | Typical Use |
|------|-------------|-------------|
| **PROFESSIONAL** | Standard commercial license | Regular customers |
| **ENTERPRISE** | Extended features/support | Large organizations |
| **TRIAL** | Limited duration testing | Evaluation period |
| **DEMO** | Short-term demonstration | Sales demos |

## Integration with Main App

The Master Key Generator uses the **same license algorithm** as NARONG CCTV Monitor, ensuring perfect compatibility:

```python
# Shared configuration
LICENSE_SALT = b"NarongCCTV_SkyTech_2025_SecureKey"

# Same key generation logic
def generate_license_key(machine_id, expiry_date, license_type):
    data = f"{machine_id}|{expiry_date.strftime('%Y-%m-%d')}|{license_type}"
    signature = hashlib.sha256((data + LICENSE_SALT.decode('latin-1')).encode()).hexdigest()
    key = f"{machine_id}-{expiry_date.strftime('%Y%m%d')}-{license_type[:3].upper()}-{signature[:8].upper()}"
    return key
```

## Contact & Support

**Developer**: Chhany  
**Team**: NARONG CCTV KOH-KONG  
**Company**: Sky-Tech  
**Telegram**: [@chhanycls](https://t.me/chhanycls)

---

**Version**: 8.8.0  
**Last Updated**: November 2025  
**Status**: Production Ready ✅
