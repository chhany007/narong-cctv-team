"""
Master Key Generator - NARONG CCTV Monitor v8.8.0
=================================================
Standalone application for administrators to generate license keys
Author: Chhany - Sky-Tech
"""

import sys
import hashlib
from datetime import datetime, timedelta
from PyQt5 import QtCore, QtGui, QtWidgets

# License configuration (must match main app)
LICENSE_SALT = b"NarongCCTV_SkyTech_2025_SecureKey"
APP_VERSION = "8.8.0"

def generate_license_key(machine_id, expiry_date, license_type="PROFESSIONAL"):
    """Generate a license key"""
    # Use abbreviated type for signature to match validation logic
    type_abbrev = license_type[:3].upper()
    data = f"{machine_id}|{expiry_date.strftime('%Y-%m-%d')}|{type_abbrev}"
    signature = hashlib.sha256((data + LICENSE_SALT.decode('latin-1')).encode()).hexdigest()
    key = f"{machine_id}-{expiry_date.strftime('%Y%m%d')}-{type_abbrev}-{signature[:8].upper()}"
    return key

class MasterKeyGeneratorApp(QtWidgets.QMainWindow):
    """Standalone Master Key Generator Application"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔑 License Key Generator")
        self.setMinimumWidth(750)
        self.setMinimumHeight(650)
        self.init_ui()
        
    def init_ui(self):
        # Central widget
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Set window background and global styles
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
                background-color: white;
                font-size: 13px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #495057;
            }
            QPushButton {
                border-radius: 6px;
                font-weight: bold;
                padding: 10px 20px;
                border: none;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            QComboBox, QSpinBox {
                border: 2px solid #ced4da;
                border-radius: 6px;
                background-color: white;
            }
            QComboBox:focus, QSpinBox:focus {
                border-color: #6f42c1;
            }
        """)
        
        # Spacer for top margin
        layout.addSpacing(10)
        
        # Machine ID input with enhanced styling
        machine_group = QtWidgets.QGroupBox("🔐 Machine ID")
        machine_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: 600;
                color: #2c3e50;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px;
            }
        """)
        machine_layout = QtWidgets.QVBoxLayout()
        machine_layout.setSpacing(12)
        machine_layout.setContentsMargins(15, 15, 15, 15)
        
        machine_label = QtWidgets.QLabel("<span style='color: #5a6c7d; font-size: 12px;'>Enter the 16-character Machine ID from user's application</span>")
        machine_layout.addWidget(machine_label)
        
        self.machine_id_input = QtWidgets.QLineEdit()
        self.machine_id_input.setPlaceholderText("Paste 16-character Machine ID here...")
        self.machine_id_input.setFont(QtGui.QFont("Courier New", 11))
        self.machine_id_input.setStyleSheet("""
            QLineEdit {
                padding: 14px 16px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: #f8f9fa;
                font-size: 13px;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border-color: #667eea;
                background-color: white;
            }
            QLineEdit:hover {
                border-color: #b8c5d6;
            }
        """)
        self.machine_id_input.textChanged.connect(self.validate_machine_id)
        machine_layout.addWidget(self.machine_id_input)
        
        # Validation label with enhanced styling
        self.machine_id_status = QtWidgets.QLabel("")
        self.machine_id_status.setStyleSheet("color: #5a6c7d; font-size: 11px; padding: 6px 4px; font-weight: 500;")
        machine_layout.addWidget(self.machine_id_status)
        
        machine_group.setLayout(machine_layout)
        layout.addWidget(machine_group)
        
        # License configuration with modern card design
        config_group = QtWidgets.QGroupBox("⚙️ License Configuration")
        config_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: 600;
                color: #2c3e50;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px;
            }
        """)
        config_layout = QtWidgets.QVBoxLayout()
        config_layout.setSpacing(15)
        config_layout.setContentsMargins(15, 15, 15, 15)
        
        # Duration selection with icon and improved layout
        duration_layout = QtWidgets.QVBoxLayout()
        duration_layout.setSpacing(8)
        duration_label = QtWidgets.QLabel("📅 <b>Duration</b>")
        duration_label.setStyleSheet("font-size: 13px; color: #2c3e50; padding: 0;")
        duration_layout.addWidget(duration_label)
        
        self.duration_combo = QtWidgets.QComboBox()
        self.duration_combo.addItems([
            "🔹 30 Days (Trial)",
            "🔹 90 Days (3 Months)",
            "🔹 180 Days (6 Months)",
            "⭐ 365 Days (1 Year)",
            "🌟 730 Days (2 Years)",
            "💎 1825 Days (5 Years)",
            "🏆 3650 Days (10 Years)",
            "⚙️ Custom Days..."
        ])
        self.duration_combo.setCurrentIndex(3)  # Default to 1 year
        self.duration_combo.setStyleSheet("""
            QComboBox {
                padding: 10px 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: #f8f9fa;
                font-size: 13px;
                color: #2c3e50;
            }
            QComboBox:hover {
                border-color: #b8c5d6;
            }
            QComboBox:focus {
                border-color: #667eea;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
        """)
        self.duration_combo.currentIndexChanged.connect(self.on_duration_changed)
        duration_layout.addWidget(self.duration_combo)
        config_layout.addLayout(duration_layout)
        
        # Custom days input with modern styling
        self.custom_days_container = QtWidgets.QWidget()
        custom_days_layout = QtWidgets.QVBoxLayout(self.custom_days_container)
        custom_days_layout.setContentsMargins(0, 8, 0, 0)
        custom_days_layout.setSpacing(8)
        custom_days_label = QtWidgets.QLabel("⚙️ <b>Custom Days</b>")
        custom_days_label.setStyleSheet("font-size: 13px; color: #2c3e50;")
        custom_days_layout.addWidget(custom_days_label)
        self.custom_days_input = QtWidgets.QSpinBox()
        self.custom_days_input.setRange(1, 36500)
        self.custom_days_input.setValue(365)
        self.custom_days_input.setStyleSheet("""
            QSpinBox {
                padding: 10px 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: #f8f9fa;
                font-size: 13px;
                color: #2c3e50;
            }
            QSpinBox:hover {
                border-color: #b8c5d6;
            }
            QSpinBox:focus {
                border-color: #667eea;
                background-color: white;
            }
        """)
        custom_days_layout.addWidget(self.custom_days_input)
        self.custom_days_container.setVisible(False)
        config_layout.addWidget(self.custom_days_container)
        
        # License type with icons and modern layout
        type_layout = QtWidgets.QVBoxLayout()
        type_layout.setSpacing(8)
        type_label = QtWidgets.QLabel("🏷️ <b>License Type</b>")
        type_label.setStyleSheet("font-size: 13px; color: #2c3e50; padding: 0;")
        type_layout.addWidget(type_label)
        
        self.type_combo = QtWidgets.QComboBox()
        self.type_combo.addItems([
            "💼 PROFESSIONAL",
            "🏢 ENTERPRISE",
            "🧪 TRIAL",
            "🎯 DEMO"
        ])
        self.type_combo.setStyleSheet("""
            QComboBox {
                padding: 10px 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: #f8f9fa;
                font-size: 13px;
                color: #2c3e50;
                font-weight: 600;
            }
            QComboBox:hover {
                border-color: #b8c5d6;
            }
            QComboBox:focus {
                border-color: #667eea;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
        """)
        type_layout.addWidget(self.type_combo)
        config_layout.addLayout(type_layout)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Generate button with enhanced gradient design
        generate_btn = QtWidgets.QPushButton("🔑 Generate License Key")
        generate_btn.setMinimumHeight(60)
        generate_btn.setCursor(QtCore.Qt.PointingHandCursor)
        generate_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                font-weight: 700;
                font-size: 15px;
                padding: 18px 30px;
                border-radius: 10px;
                border: none;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5568d3, stop:1 #6941a0);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a5bbd, stop:1 #583890);
                padding: 19px 30px 17px 30px;
            }
        """)
        generate_btn.clicked.connect(self.generate_key)
        layout.addWidget(generate_btn)
        
        # Generated key display with modern card design
        result_group = QtWidgets.QGroupBox("✨ Generated License Key")
        result_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: 600;
                color: #2c3e50;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px;
            }
        """)
        result_layout = QtWidgets.QVBoxLayout()
        result_layout.setSpacing(12)
        result_layout.setContentsMargins(15, 15, 15, 15)
        
        self.generated_key_display = QtWidgets.QTextEdit()
        self.generated_key_display.setReadOnly(True)
        self.generated_key_display.setFont(QtGui.QFont("Consolas", 12, QtGui.QFont.Bold))
        self.generated_key_display.setStyleSheet("""
            QTextEdit {
                background-color: #f0f8ff;
                border: 2px solid #667eea;
                border-radius: 8px;
                padding: 16px;
                color: #2c3e50;
                font-weight: 600;
                line-height: 1.6;
            }
            QTextEdit:focus {
                border-color: #764ba2;
            }
        """)
        self.generated_key_display.setPlaceholderText(
            "🔑 License Key Will Appear Here\n\n"
            "Follow these steps:\n"
            "1️⃣ Enter Machine ID\n"
            "2️⃣ Choose duration & type\n"
            "3️⃣ Click Generate button\n"
        )
        self.generated_key_display.setMinimumHeight(140)
        result_layout.addWidget(self.generated_key_display)
        
        # Action buttons with modern card-like design
        action_layout = QtWidgets.QHBoxLayout()
        action_layout.setSpacing(12)
        
        copy_key_btn = QtWidgets.QPushButton("📋 Copy")
        copy_key_btn.setMinimumHeight(48)
        copy_key_btn.setCursor(QtCore.Qt.PointingHandCursor)
        copy_key_btn.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                font-weight: 600;
                font-size: 13px;
                padding: 12px 24px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #138496;
            }
            QPushButton:pressed {
                background-color: #117a8b;
                padding: 13px 24px 11px 24px;
            }
        """)
        copy_key_btn.clicked.connect(self.copy_generated_key)
        action_layout.addWidget(copy_key_btn)
        
        save_btn = QtWidgets.QPushButton("💾 Save")
        save_btn.setMinimumHeight(48)
        save_btn.setCursor(QtCore.Qt.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-weight: 600;
                font-size: 13px;
                padding: 12px 24px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
                padding: 13px 24px 11px 24px;
            }
        """)
        save_btn.clicked.connect(self.save_to_file)
        action_layout.addWidget(save_btn)
        
        clear_btn = QtWidgets.QPushButton("🗑️ Clear")
        clear_btn.setMinimumHeight(48)
        clear_btn.setCursor(QtCore.Qt.PointingHandCursor)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                font-weight: 600;
                font-size: 13px;
                padding: 12px 24px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #545b62;
                padding: 13px 24px 11px 24px;
            }
        """)
        clear_btn.clicked.connect(self.clear_form)
        action_layout.addWidget(clear_btn)
        
        result_layout.addLayout(action_layout)
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)
        
        # Status bar
        self.statusBar().showMessage("Ready to generate license keys")
        
        # Menu bar
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        save_action = QtWidgets.QAction("💾 Save Key to File", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_to_file)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QtWidgets.QAction("❌ Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QtWidgets.QAction("ℹ️ About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        contact_action = QtWidgets.QAction("📱 Contact Support", self)
        contact_action.triggered.connect(self.show_contact)
        help_menu.addAction(contact_action)
    
    def validate_machine_id(self):
        """Validate machine ID as user types"""
        machine_id = self.machine_id_input.text().strip()
        
        if not machine_id:
            self.machine_id_status.setText("")
            return
        
        if len(machine_id) < 16:
            self.machine_id_status.setText(f"⚠️ Too short ({len(machine_id)}/16 characters)")
            self.machine_id_status.setStyleSheet("color: #856404; font-size: 11px; padding: 4px;")
        elif len(machine_id) > 16:
            self.machine_id_status.setText(f"❌ Too long ({len(machine_id)}/16 characters)")
            self.machine_id_status.setStyleSheet("color: #dc3545; font-size: 11px; padding: 4px;")
        else:
            self.machine_id_status.setText("✅ Valid Machine ID")
            self.machine_id_status.setStyleSheet("color: #28a745; font-size: 11px; padding: 4px;")
    
    def on_duration_changed(self, index):
        """Show/hide custom days input based on duration selection"""
        self.custom_days_container.setVisible(index == 7)  # "Custom Days..."
    
    def generate_key(self):
        """Generate license key based on configuration"""
        machine_id = self.machine_id_input.text().strip()
        
        if not machine_id:
            QtWidgets.QMessageBox.warning(self, "Missing Information", 
                "Please enter the target Machine ID.\n\nYou can get this from the user's license activation dialog.")
            self.machine_id_input.setFocus()
            return
        
        if len(machine_id) != 16:
            QtWidgets.QMessageBox.warning(self, "Invalid Machine ID", 
                f"Machine ID must be exactly 16 characters.\n\nCurrent length: {len(machine_id)}\n\nPlease verify the ID from the user.")
            self.machine_id_input.setFocus()
            return
        
        # Get duration
        duration_index = self.duration_combo.currentIndex()
        duration_map = {
            0: 30,      # 30 days
            1: 90,      # 3 months
            2: 180,     # 6 months
            3: 365,     # 1 year
            4: 730,     # 2 years
            5: 1825,    # 5 years
            6: 3650,    # 10 years
            7: self.custom_days_input.value()  # Custom
        }
        days = duration_map[duration_index]
        
        # Calculate expiry date
        expiry_date = datetime.now() + timedelta(days=days)
        
        # Get license type
        license_type = self.type_combo.currentText()
        
        # Generate key
        license_key = generate_license_key(machine_id, expiry_date, license_type)
        
        # Display result
        result_text = "=" * 60 + "\n"
        result_text += f"LICENSE KEY GENERATED SUCCESSFULLY\n"
        result_text += "=" * 60 + "\n\n"
        result_text += f"License Key:\n{license_key}\n\n"
        result_text += f"Machine ID:    {machine_id}\n"
        result_text += f"License Type:  {license_type}\n"
        result_text += f"Duration:      {days} days\n"
        result_text += f"Expires On:    {expiry_date.strftime('%Y-%m-%d')}\n"
        result_text += f"Generated:     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        result_text += "\n" + "=" * 60 + "\n"
        result_text += "📋 Copy this key and send it to the user\n"
        result_text += "=" * 60
        
        self.generated_key_display.setPlainText(result_text)
        
        # Update status bar
        self.statusBar().showMessage(f"✅ License key generated successfully! Type: {license_type}, Duration: {days} days", 5000)
        
        # Show success message
        QtWidgets.QMessageBox.information(self, "Success", 
            f"License key generated successfully!\n\n"
            f"Type: {license_type}\n"
            f"Duration: {days} days\n"
            f"Expires: {expiry_date.strftime('%Y-%m-%d')}\n\n"
            f"The key has been displayed in the text area.\n"
            f"Click 'Copy License Key' to copy it to clipboard.")
    
    def copy_generated_key(self):
        """Copy generated license key to clipboard"""
        text = self.generated_key_display.toPlainText()
        if not text or "will appear here" in text:
            QtWidgets.QMessageBox.warning(self, "No Key Generated", 
                "Please generate a license key first.")
            return
        
        # Extract just the key (look for the line after "License Key:")
        lines = text.split('\n')
        key_line = None
        for i, line in enumerate(lines):
            if "License Key:" in line and i + 1 < len(lines):
                key_line = lines[i + 1].strip()
                break
        
        if key_line:
            QtWidgets.QApplication.clipboard().setText(key_line)
            self.statusBar().showMessage("✅ License key copied to clipboard!", 3000)
            QtWidgets.QMessageBox.information(self, "Copied", 
                "License key copied to clipboard!\n\nYou can now send it to the user via:\n• Telegram\n• Email\n• Other messaging apps")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Could not extract license key from text.")
    
    def save_to_file(self):
        """Save generated key to file"""
        text = self.generated_key_display.toPlainText()
        if not text or "will appear here" in text:
            QtWidgets.QMessageBox.warning(self, "No Key Generated", 
                "Please generate a license key first.")
            return
        
        # Suggest filename based on machine ID and date
        machine_id = self.machine_id_input.text().strip()[:8]
        date_str = datetime.now().strftime('%Y%m%d')
        suggested_name = f"license_key_{machine_id}_{date_str}.txt"
        
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save License Key",
            suggested_name,
            "Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(text)
                self.statusBar().showMessage(f"✅ License key saved to {filename}", 5000)
                QtWidgets.QMessageBox.information(self, "Saved", 
                    f"License key saved successfully!\n\nFile: {filename}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", 
                    f"Failed to save file:\n{str(e)}")
    
    def clear_form(self):
        """Clear all fields"""
        reply = QtWidgets.QMessageBox.question(self, "Clear Form", 
            "Are you sure you want to clear all fields?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        
        if reply == QtWidgets.QMessageBox.Yes:
            self.machine_id_input.clear()
            self.generated_key_display.clear()
            self.duration_combo.setCurrentIndex(3)
            self.type_combo.setCurrentIndex(0)
            self.machine_id_status.setText("")
            self.statusBar().showMessage("Form cleared", 2000)
            self.machine_id_input.setFocus()
    
    def show_about(self):
        """Show about dialog"""
        QtWidgets.QMessageBox.about(self, "About Master Key Generator",
            f"<h2>🔑 Master Key Generator</h2>"
            f"<p><b>Version:</b> {APP_VERSION}</p>"
            f"<p><b>Application:</b> NARONG CCTV Monitor</p>"
            f"<p><b>Purpose:</b> Generate license keys for application users</p>"
            f"<hr>"
            f"<p><b>Developer:</b> Chhany</p>"
            f"<p><b>Team:</b> NARONG CCTV KOH-KONG</p>"
            f"<p><b>Company:</b> Sky-Tech</p>"
        )
    
    def show_contact(self):
        """Show contact information"""
        reply = QtWidgets.QMessageBox.question(self, "Contact Support",
            "<h3>📱 Sky-Tech Support</h3>"
            "<p><b>Telegram:</b> @chhanycls</p>"
            "<p>Would you like to open Telegram now?</p>",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        
        if reply == QtWidgets.QMessageBox.Yes:
            import webbrowser
            webbrowser.open('https://t.me/chhanycls')

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set application icon if available
    try:
        app.setWindowIcon(QtGui.QIcon("key.ico"))
    except:
        pass
    
    window = MasterKeyGeneratorApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
