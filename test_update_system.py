"""
Test the update system locally
Run this to simulate an update check without needing a server
"""

import json
import os
from update_manager import UpdateChecker, UpdateInfo, UpdateDialog
from PyQt5 import QtWidgets
import sys

def create_test_version_file():
    """Create a local test version.json file"""
    test_version = {
        "version": "8.1.0",
        "download_url": "https://github.com/test/test/releases/download/v8.1.0/NARONG_CCTV_TEAM.exe",
        "release_notes": """🎉 What's New in v8.1.0 (TEST VERSION):

✨ New Features:
  • Enhanced SADP discovery performance
  • Improved NVR camera fetching  
  • Better error handling for network timeouts
  • Added batch camera status checking
  • Automatic update system!

🐛 Bug Fixes:
  • Fixed issue with NVR login on some models
  • Resolved camera list refresh bug
  • Improved Excel sheet detection

⚡ Performance:
  • Faster parallel camera checking
  • Reduced memory usage
  • Optimized network scans

📝 Other Improvements:
  • Updated UI styling
  • Better logging system
  • Enhanced credential management""",
        "release_date": "2025-11-20",
        "file_size": 108000000,
        "checksum": "test_checksum_not_for_production",
        "required": False
    }
    
    with open("test_version.json", "w") as f:
        json.dump(test_version, f, indent=2)
    
    print("✅ Created test_version.json")

def test_version_comparison():
    """Test version comparison logic"""
    print("\n=== Testing Version Comparison ===")
    checker = UpdateChecker()
    
    tests = [
        ("8.0.0", "8.1.0", -1),  # Current < New = Update available
        ("8.1.0", "8.0.0", 1),   # Current > New = No update
        ("8.0.0", "8.0.0", 0),   # Current = New = No update
        ("7.9.9", "8.0.0", -1),  # Major version bump
        ("8.0.0", "8.0.1", -1),  # Patch update
    ]
    
    for v1, v2, expected in tests:
        result = checker.compare_versions(v1, v2)
        status = "✅" if result == expected else "❌"
        print(f"{status} compare({v1}, {v2}) = {result} (expected {expected})")

def test_update_dialog():
    """Test the update dialog UI"""
    print("\n=== Testing Update Dialog ===")
    
    # Create test update info
    test_data = {
        "version": "8.1.0",
        "download_url": "https://test.com/update.exe",
        "release_notes": "Test release notes:\n• Feature 1\n• Feature 2\n• Bug fix 1",
        "release_date": "2025-11-20",
        "file_size": 108000000,
        "checksum": "test_checksum",
        "required": False
    }
    
    app = QtWidgets.QApplication(sys.argv)
    update_info = UpdateInfo(test_data)
    dialog = UpdateDialog(update_info)
    
    print("✅ Update dialog created successfully")
    print("   Opening dialog... (Close it to continue)")
    
    dialog.exec_()
    print("✅ Dialog closed")

def test_config_load():
    """Test configuration loading"""
    print("\n=== Testing Configuration ===")
    
    checker = UpdateChecker()
    config = checker.load_config()
    
    print(f"Current Version: {config.get('current_version')}")
    print(f"App Name: {config.get('app_name')}")
    print(f"Update URL: {config.get('update_check_url')}")
    print(f"Check on Startup: {config.get('check_on_startup')}")
    print(f"Auto Download: {config.get('auto_download')}")
    
    if not config.get('update_check_url'):
        print("\n⚠️  Warning: update_check_url is not configured!")
        print("   Edit version_config.json to add your update server URL")
    
    print("✅ Configuration loaded successfully")

def test_full_flow():
    """Test the complete update check flow"""
    print("\n=== Testing Full Update Flow ===")
    
    # Lower current version to trigger update
    checker = UpdateChecker()
    original_version = checker.config.get('current_version')
    checker.config['current_version'] = '7.0.0'
    
    print(f"Temporarily set current version to 7.0.0 (was {original_version})")
    print("This should trigger an update notification...")
    
    # Create test update info
    test_data = {
        "version": "8.1.0",
        "download_url": "https://test.com/update.exe",
        "release_notes": "🎉 Test Update Available!\n\n✨ New Features:\n  • Feature 1\n  • Feature 2",
        "release_date": "2025-11-20",
        "file_size": 108000000,
        "checksum": "test",
        "required": False
    }
    
    app = QtWidgets.QApplication(sys.argv)
    update_info = UpdateInfo(test_data)
    
    # Show dialog
    dialog = UpdateDialog(update_info)
    print("✅ Showing update dialog...")
    print("   (The download won't work - it's just a test)")
    
    result = dialog.exec_()
    
    if result == QtWidgets.QDialog.Accepted:
        print("✅ User accepted update")
    else:
        print("ℹ️  User declined/closed update")
    
    # Restore original version
    checker.config['current_version'] = original_version
    print(f"✅ Restored version to {original_version}")

def main():
    print("=" * 60)
    print("  UPDATE SYSTEM TEST SUITE")
    print("=" * 60)
    
    # Run tests
    try:
        create_test_version_file()
        test_version_comparison()
        test_config_load()
        
        print("\n" + "=" * 60)
        print("Basic tests passed! ✅")
        print("=" * 60)
        
        # Ask if user wants to test UI
        response = input("\nTest update dialog UI? (y/n): ").lower()
        if response == 'y':
            test_update_dialog()
        
        # Ask if user wants to test full flow
        response = input("\nTest complete update flow? (y/n): ").lower()
        if response == 'y':
            test_full_flow()
        
        print("\n" + "=" * 60)
        print("All tests completed! ✅")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Configure update_check_url in version_config.json")
        print("2. Upload version.json to your server")
        print("3. Build exe: .\\build_complete.bat")
        print("4. Test with real update server")
        print("\nSee UPDATE_SYSTEM_SETUP.md for complete instructions.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
