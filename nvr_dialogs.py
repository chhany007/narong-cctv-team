# NVR Management Dialogs for CameraMonitor
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import threading
import ipaddress

class AddNVRDialog(QDialog):
    """Dialog for adding new NVR with credentials"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New NVR")
        self.setWindowIcon(QIcon("nvr.ico") if os.path.exists("nvr.ico") else QIcon())
        self.setModal(True)
        self.setFixedSize(450, 350)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("🗄️ Add New NVR Configuration")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Form layout
        form_layout = QFormLayout()
        
        # NVR Name
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g., NVR20, Main Building NVR")
        form_layout.addRow("📝 NVR Name:", self.name_edit)
        
        # IP Address
        self.ip_edit = QLineEdit()
        self.ip_edit.setPlaceholderText("192.168.x.x")
        form_layout.addRow("🌐 IP Address:", self.ip_edit)
        
        # Port
        self.port_edit = QLineEdit("80")
        self.port_edit.setPlaceholderText("80, 8080, 443")
        form_layout.addRow("🔌 Port:", self.port_edit)
        
        # Protocol
        self.protocol_combo = QComboBox()
        self.protocol_combo.addItems(["HTTP", "HTTPS"])
        form_layout.addRow("🔒 Protocol:", self.protocol_combo)
        
        # Username
        self.username_edit = QLineEdit("admin")
        self.username_edit.setPlaceholderText("admin, administrator")
        form_layout.addRow("👤 Username:", self.username_edit)
        
        # Password
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText("Enter password")
        form_layout.addRow("🔑 Password:", self.password_edit)
        
        layout.addLayout(form_layout)
        
        # Test connection button
        self.test_btn = QPushButton("🔍 Test Connection")
        self.test_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.test_btn.clicked.connect(self.test_connection)
        layout.addWidget(self.test_btn)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("💾 Save NVR")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        self.save_btn.clicked.connect(self.accept)
        
        self.cancel_btn = QPushButton("❌ Cancel")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def test_connection(self):
        """Test NVR connection"""
        if not self.validate_input():
            return
            
        self.test_btn.setEnabled(False)
        self.test_btn.setText("🔄 Testing...")
        self.status_label.setText("Testing connection...")
        self.status_label.setStyleSheet("color: #f39c12;")
        
        # Run test in thread
        thread = threading.Thread(target=self._test_connection_thread)
        thread.daemon = True
        thread.start()
        
    def _test_connection_thread(self):
        """Test connection in background thread"""
        try:
            protocol = self.protocol_combo.currentText().lower()
            ip = self.ip_edit.text().strip()
            port = self.port_edit.text().strip()
            username = self.username_edit.text().strip()
            password = self.password_edit.text().strip()
            
            url = f"{protocol}://{ip}:{port}/ISAPI/System/deviceInfo"
            
            auth_methods = [HTTPBasicAuth(username, password), HTTPDigestAuth(username, password)]
            
            for auth in auth_methods:
                try:
                    response = requests.get(url, auth=auth, timeout=5, verify=False)
                    if response.status_code == 200:
                        QTimer.singleShot(0, lambda: self._show_test_result(True, f"✅ Connection successful ({auth.__class__.__name__.replace('HTTP', '').replace('Auth', '')})"))
                        return
                except:
                    continue
                    
            QTimer.singleShot(0, lambda: self._show_test_result(False, "❌ Connection failed - check credentials and network"))
            
        except Exception as e:
            QTimer.singleShot(0, lambda: self._show_test_result(False, f"❌ Error: {str(e)}"))
            
    def _show_test_result(self, success, message):
        """Show test result in UI thread"""
        self.test_btn.setEnabled(True)
        self.test_btn.setText("🔍 Test Connection")
        self.status_label.setText(message)
        
        if success:
            self.status_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            self.status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
            
    def validate_input(self):
        """Validate form input"""
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Invalid Input", "Please enter NVR name")
            return False
            
        if not self.ip_edit.text().strip():
            QMessageBox.warning(self, "Invalid Input", "Please enter IP address")
            return False
            
        try:
            ipaddress.ip_address(self.ip_edit.text().strip())
        except:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid IP address")
            return False
            
        try:
            port = int(self.port_edit.text().strip())
            if not (1 <= port <= 65535):
                raise ValueError
        except:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid port (1-65535)")
            return False
            
        if not self.username_edit.text().strip():
            QMessageBox.warning(self, "Invalid Input", "Please enter username")
            return False
            
        if not self.password_edit.text().strip():
            QMessageBox.warning(self, "Invalid Input", "Please enter password")
            return False
            
        return True
        
    def get_nvr_data(self):
        """Get NVR configuration data"""
        return {
            'name': self.name_edit.text().strip(),
            'ip': self.ip_edit.text().strip(),
            'port': int(self.port_edit.text().strip()),
            'protocol': self.protocol_combo.currentText().lower(),
            'username': self.username_edit.text().strip(),
            'password': self.password_edit.text().strip()
        }

class EditNVRDialog(AddNVRDialog):
    """Dialog for editing existing NVR credentials"""
    def __init__(self, nvr_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit NVR Credentials")
        # Update title label
        title_widgets = self.findChildren(QLabel)
        for widget in title_widgets:
            if "Add New NVR" in widget.text():
                widget.setText("🔧 Edit NVR Credentials")
                break
        
        self.nvr_data = nvr_data
        self.populate_fields()
        
    def populate_fields(self):
        """Populate fields with existing NVR data"""
        self.name_edit.setText(self.nvr_data.get('name', ''))
        self.name_edit.setEnabled(False)  # Don't allow name changes
        self.ip_edit.setText(self.nvr_data.get('ip', ''))
        self.port_edit.setText(str(self.nvr_data.get('port', 80)))
        
        protocol = self.nvr_data.get('protocol', 'http').upper()
        index = self.protocol_combo.findText(protocol)
        if index >= 0:
            self.protocol_combo.setCurrentIndex(index)
            
        self.username_edit.setText(self.nvr_data.get('username', 'admin'))
        self.password_edit.setText(self.nvr_data.get('password', ''))