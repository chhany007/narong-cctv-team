"""
Automatic Updater Script
This script runs after the main app closes to replace the old EXE with the new one
"""

import os
import sys
import time
import shutil
import subprocess

def update_application(old_exe_path, new_exe_path):
    """Replace old EXE with new one and restart"""
    print(f"Updater started...")
    print(f"Old EXE: {old_exe_path}")
    print(f"New EXE: {new_exe_path}")
    
    # Wait for old process to fully close
    print("Waiting for application to close...")
    time.sleep(2)
    
    # Backup old file
    backup_path = old_exe_path + ".backup"
    try:
        if os.path.exists(old_exe_path):
            print(f"Backing up old file to: {backup_path}")
            shutil.copy2(old_exe_path, backup_path)
        
        # Replace with new file
        print(f"Replacing old file with new version...")
        shutil.copy2(new_exe_path, old_exe_path)
        
        # Delete backup if successful
        if os.path.exists(backup_path):
            os.remove(backup_path)
        
        # Delete temp file
        if os.path.exists(new_exe_path):
            os.remove(new_exe_path)
        
        print("Update successful!")
        
        # Restart application
        print(f"Restarting application...")
        time.sleep(1)
        subprocess.Popen([old_exe_path], shell=False)
        
        return True
        
    except Exception as e:
        print(f"Update failed: {e}")
        # Restore backup if exists
        if os.path.exists(backup_path):
            print("Restoring backup...")
            shutil.copy2(backup_path, old_exe_path)
            os.remove(backup_path)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: updater.py <old_exe_path> <new_exe_path>")
        sys.exit(1)
    
    old_exe = sys.argv[1]
    new_exe = sys.argv[2]
    
    success = update_application(old_exe, new_exe)
    sys.exit(0 if success else 1)
