"""
Update Manager for Camera Monitor
Handles version checking, downloading, and installing updates
"""

import os
import sys
import json
import requests
import subprocess
import time
import hashlib
from datetime import datetime
from PyQt5 import QtCore, QtWidgets, QtGui

VERSION_CONFIG_FILE = "version_config.json"
UPDATE_CACHE_FILE = "update_cache.json"
LAST_CHECK_FILE = "last_update_check.json"

class UpdateInfo:
    def __init__(self, data):
        self.version = data.get("version", "0.0.0")
        self.download_url = data.get("download_url", "")
        self.release_notes = data.get("release_notes", "")
        self.release_date = data.get("release_date", "")
        self.file_size = data.get("file_size", 0)
        self.checksum = data.get("checksum", "")
        self.required = data.get("required", False)

class UpdateChecker:
    def __init__(self):
        self.config = self.load_config()
        
    def load_config(self):
        """Load version configuration"""
        try:
            if os.path.exists(VERSION_CONFIG_FILE):
                with open(VERSION_CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
        
        # Default config
        return {
            "current_version": "8.0.0",
            "app_name": "NARONG CCTV TEAM - Camera Monitor",
            "update_check_url": "",
            "check_on_startup": True,
            "auto_download": False
        }
    
    def save_config(self):
        """Save version configuration"""
        try:
            with open(VERSION_CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get_current_version(self):
        """Get current application version"""
        return self.config.get("current_version", "8.0.0")
    
    def compare_versions(self, version1, version2):
        """Compare two version strings (returns 1 if v1 > v2, -1 if v1 < v2, 0 if equal)"""
        try:
            v1_parts = [int(x) for x in version1.split('.')]
            v2_parts = [int(x) for x in version2.split('.')]
            
            # Pad with zeros if needed
            while len(v1_parts) < 3:
                v1_parts.append(0)
            while len(v2_parts) < 3:
                v2_parts.append(0)
            
            for i in range(3):
                if v1_parts[i] > v2_parts[i]:
                    return 1
                elif v1_parts[i] < v2_parts[i]:
                    return -1
            
            return 0
        except Exception:
            return 0
    
    def should_check_for_updates(self):
        """Determine if we should check for updates (based on last check time)"""
        if not self.config.get("check_on_startup", True):
            return False
        
        try:
            if os.path.exists(LAST_CHECK_FILE):
                with open(LAST_CHECK_FILE, 'r') as f:
                    data = json.load(f)
                    last_check = data.get("timestamp", 0)
                    # Check at most once per day
                    if time.time() - last_check < 86400:
                        return False
        except Exception:
            pass
        
        return True
    
    def save_last_check_time(self):
        """Save the last update check timestamp"""
        try:
            with open(LAST_CHECK_FILE, 'w') as f:
                json.dump({"timestamp": time.time()}, f)
        except Exception as e:
            print(f"Error saving last check time: {e}")
    
    def check_for_updates(self, timeout=10):
        """Check for available updates from remote server"""
        try:
            update_url = self.config.get("update_check_url", "")
            if not update_url:
                return None, "Update URL not configured"
            
            response = requests.get(update_url, timeout=timeout)
            if response.status_code != 200:
                return None, f"Server returned status {response.status_code}"
            
            update_data = response.json()
            update_info = UpdateInfo(update_data)
            
            # Compare versions
            current = self.get_current_version()
            if self.compare_versions(update_info.version, current) > 0:
                self.save_last_check_time()
                return update_info, None
            else:
                self.save_last_check_time()
                return None, "Already on latest version"
                
        except requests.exceptions.Timeout:
            return None, "Connection timeout"
        except requests.exceptions.ConnectionError:
            return None, "Could not connect to update server"
        except Exception as e:
            return None, f"Error checking for updates: {str(e)}"
    
    def download_update(self, update_info, progress_callback=None):
        """Download update file with progress tracking"""
        try:
            response = requests.get(update_info.download_url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            # Save to temp directory
            temp_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Temp')
            download_path = os.path.join(temp_dir, f"NARONG_CCTV_Update_{update_info.version}.exe")
            
            with open(download_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback and total_size > 0:
                            progress_callback(int(downloaded * 100 / total_size))
            
            # Verify checksum if provided
            if update_info.checksum:
                if not self.verify_checksum(download_path, update_info.checksum):
                    os.remove(download_path)
                    return None, "Checksum verification failed"
            
            return download_path, None
            
        except Exception as e:
            return None, f"Download failed: {str(e)}"
    
    def verify_checksum(self, filepath, expected_checksum):
        """Verify file checksum (SHA256)"""
        try:
            sha256_hash = hashlib.sha256()
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            
            return sha256_hash.hexdigest().lower() == expected_checksum.lower()
        except Exception:
            return False
    
    def install_update(self, installer_path):
        """Launch installer and exit current application"""
        try:
            # Launch installer with elevated privileges
            subprocess.Popen([installer_path], shell=True)
            return True, None
        except Exception as e:
            return False, f"Failed to launch installer: {str(e)}"


class UpdateDialog(QtWidgets.QDialog):
    """Update dialog UI"""
    
    def __init__(self, update_info, parent=None):
        super().__init__(parent)
        self.update_info = update_info
        self.installer_path = None
        self.update_checker = UpdateChecker()
        
        self.setWindowTitle("Update Available")
        self.setWindowIcon(self.style().standardIcon(QtWidgets.QStyle.SP_BrowserReload))
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Header with icon
        header_layout = QtWidgets.QHBoxLayout()
        icon_label = QtWidgets.QLabel()
        icon_label.setPixmap(self.style().standardIcon(QtWidgets.QStyle.SP_MessageBoxInformation).pixmap(48, 48))
        header_layout.addWidget(icon_label)
        
        header_text = QtWidgets.QLabel(f"<h2>Update Available!</h2>")
        header_layout.addWidget(header_text)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Version info
        version_group = QtWidgets.QGroupBox("Version Information")
        version_layout = QtWidgets.QFormLayout(version_group)
        
        current_version = self.update_checker.get_current_version()
        version_layout.addRow("Current Version:", QtWidgets.QLabel(f"<b>{current_version}</b>"))
        version_layout.addRow("New Version:", QtWidgets.QLabel(f"<b style='color: green;'>{self.update_info.version}</b>"))
        version_layout.addRow("Release Date:", QtWidgets.QLabel(self.update_info.release_date))
        
        if self.update_info.file_size > 0:
            size_mb = self.update_info.file_size / (1024 * 1024)
            version_layout.addRow("Download Size:", QtWidgets.QLabel(f"{size_mb:.1f} MB"))
        
        layout.addWidget(version_group)
        
        # Release notes
        notes_group = QtWidgets.QGroupBox("What's New")
        notes_layout = QtWidgets.QVBoxLayout(notes_group)
        
        self.notes_text = QtWidgets.QTextEdit()
        self.notes_text.setReadOnly(True)
        self.notes_text.setPlainText(self.update_info.release_notes)
        notes_layout.addWidget(self.notes_text)
        
        layout.addWidget(notes_group)
        
        # Progress bar (hidden initially)
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QtWidgets.QLabel()
        self.status_label.setVisible(False)
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        
        self.download_btn = QtWidgets.QPushButton("📥 Download & Install")
        self.download_btn.setStyleSheet("QPushButton { background-color: #27ae60; color: white; padding: 8px 16px; font-weight: bold; }")
        self.download_btn.clicked.connect(self.start_download)
        button_layout.addWidget(self.download_btn)
        
        self.later_btn = QtWidgets.QPushButton("⏰ Remind Me Later")
        self.later_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.later_btn)
        
        if not self.update_info.required:
            self.skip_btn = QtWidgets.QPushButton("❌ Skip This Version")
            self.skip_btn.clicked.connect(self.skip_version)
            button_layout.addWidget(self.skip_btn)
        
        layout.addLayout(button_layout)
    
    def start_download(self):
        """Start downloading the update"""
        self.download_btn.setEnabled(False)
        self.later_btn.setEnabled(False)
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setVisible(True)
        self.status_label.setText("Downloading update...")
        
        # Start download in background thread
        self.download_thread = DownloadThread(self.update_info, self.update_checker)
        self.download_thread.progress.connect(self.update_progress)
        self.download_thread.finished_signal.connect(self.download_finished)
        self.download_thread.start()
    
    def update_progress(self, percent):
        """Update download progress"""
        self.progress_bar.setValue(percent)
        self.status_label.setText(f"Downloading update... {percent}%")
    
    def download_finished(self, success, installer_path, error_message):
        """Handle download completion"""
        if success:
            self.installer_path = installer_path
            self.status_label.setText("✅ Download complete!")
            
            # Show install button
            self.download_btn.setText("🚀 Install Now")
            self.download_btn.setEnabled(True)
            self.download_btn.clicked.disconnect()
            self.download_btn.clicked.connect(self.install_update)
            
            self.later_btn.setText("Install Later")
            self.later_btn.setEnabled(True)
        else:
            self.status_label.setText(f"❌ Download failed: {error_message}")
            self.status_label.setStyleSheet("color: red;")
            self.download_btn.setEnabled(True)
            self.download_btn.setText("🔄 Retry Download")
            self.later_btn.setEnabled(True)
    
    def install_update(self):
        """Install the downloaded update"""
        if self.installer_path and os.path.exists(self.installer_path):
            reply = QtWidgets.QMessageBox.question(
                self, 
                "Install Update",
                "The application will now close and the installer will start.\n\nContinue?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            
            if reply == QtWidgets.QMessageBox.Yes:
                success, error = self.update_checker.install_update(self.installer_path)
                if success:
                    self.accept()
                    QtWidgets.QApplication.quit()
                else:
                    QtWidgets.QMessageBox.critical(self, "Error", error)
    
    def skip_version(self):
        """Skip this version"""
        # Save skipped version to config
        try:
            config = self.update_checker.load_config()
            config['skipped_version'] = self.update_info.version
            with open(VERSION_CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception:
            pass
        
        self.reject()


class DownloadThread(QtCore.QThread):
    """Background thread for downloading updates"""
    
    progress = QtCore.pyqtSignal(int)
    finished_signal = QtCore.pyqtSignal(bool, str, str)  # success, path, error
    
    def __init__(self, update_info, update_checker):
        super().__init__()
        self.update_info = update_info
        self.update_checker = update_checker
    
    def run(self):
        """Download the update"""
        def progress_callback(percent):
            self.progress.emit(percent)
        
        installer_path, error = self.update_checker.download_update(
            self.update_info, 
            progress_callback
        )
        
        if installer_path:
            self.finished_signal.emit(True, installer_path, "")
        else:
            self.finished_signal.emit(False, "", error)


class CheckThread(QtCore.QThread):
    """Background thread for checking updates"""
    result = QtCore.pyqtSignal(object, str)
    
    def __init__(self, checker):
        super().__init__()
        self.checker = checker
    
    def run(self):
        update_info, error = self.checker.check_for_updates()
        self.result.emit(update_info, error)


def check_for_updates_async(parent_widget=None, show_no_update=False):
    """Check for updates asynchronously and show dialog if available"""
    checker = UpdateChecker()
    
    # Check if we should check (respects last check time)
    if not show_no_update and not checker.should_check_for_updates():
        return
    
    # Show checking dialog
    progress = QtWidgets.QProgressDialog(
        "Checking for updates...",
        None,
        0, 0,
        parent_widget
    )
    progress.setWindowTitle("Update Check")
    progress.setWindowModality(QtCore.Qt.WindowModal)
    progress.setMinimumDuration(0)
    progress.setCancelButton(None)
    progress.show()
    
    def on_check_complete(update_info, error):
        progress.close()
        
        if update_info:
            # Check if this version was skipped
            config = checker.load_config()
            if config.get('skipped_version') == update_info.version:
                if not show_no_update:
                    return
            
            # Show update dialog
            dialog = UpdateDialog(update_info, parent_widget)
            dialog.exec_()
        else:
            if show_no_update:
                if error:
                    QtWidgets.QMessageBox.information(
                        parent_widget,
                        "Update Check",
                        f"Could not check for updates:\n{error}"
                    )
                else:
                    QtWidgets.QMessageBox.information(
                        parent_widget,
                        "No Updates",
                        "You are already using the latest version!"
                    )
    
    check_thread = CheckThread(checker)
    check_thread.result.connect(on_check_complete)
    check_thread.finished.connect(check_thread.deleteLater)  # Clean up when done
    check_thread.start()
    
    # Keep reference to prevent garbage collection
    if not hasattr(parent_widget, '_update_threads'):
        parent_widget._update_threads = []
    parent_widget._update_threads.append(check_thread)
