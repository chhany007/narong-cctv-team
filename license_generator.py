"""
NARONG CCTV License Key Generator
Master tool for generating and managing license keys
"""

import hashlib
import secrets
import json
from datetime import datetime, timedelta
import base64
import sys
from PyQt5 import QtWidgets, QtCore, QtGui

LICENSE_SALT = b"NarongCCTV_SkyTech_2025_SecureKey"

class LicenseGenerator:
    """Generate license keys with encryption and validation"""
    
    MASTER_SECRET = "NARONG_CCTV_2025_MASTER_KEY_v8.7_SECURE"  # Keep this secret!
    
    @staticmethod
    def generate_license_key(
        company_name: str,
        expiration_days: int = 365,
        max_activations: int = 1,
        features: list = None,
        machine_id: str | None = None,
        license_type: str = "PROFESSIONAL"
    ) -> dict:
        """
        Generate a license key with metadata
        
        Args:
            company_name: Customer company name
            expiration_days: Days until license expires
            max_activations: Maximum number of machine activations
            features: List of enabled features (None = all features)
            
        Returns:
            Dictionary with license key and metadata, including
            a machine-bound activation key when a Machine ID is provided
        """
        if features is None:
            features = ["full_access"]
        
        # Generate unique license ID
        license_id = secrets.token_hex(8).upper()
        
        # Calculate expiration date
        issue_date = datetime.now()
        expiration_date = issue_date + timedelta(days=expiration_days)
        
        # Create license data
        license_data = {
            "license_id": license_id,
            "company_name": company_name,
            "issue_date": issue_date.isoformat(),
            "expiration_date": expiration_date.isoformat(),
            "max_activations": max_activations,
            "features": features,
            "version": "8.6"
        }
        
        if machine_id:
            license_data["machine_id"] = machine_id
        else:
            license_data["machine_id"] = ""

        # Generate signature
        signature = LicenseGenerator._generate_signature(license_data)
        license_data["signature"] = signature
        
        # Encode license key
        license_key = LicenseGenerator._encode_license(license_data)

        # Generate activation key bound to machine (if provided)
        activation_key = None
        if machine_id:
            activation_key = LicenseGenerator._build_activation_key(
                machine_id,
                expiration_date,
                license_type
            )
        
        return {
            "license_key": license_key,
            "license_id": license_id,
            "company_name": company_name,
            "issue_date": issue_date.strftime("%Y-%m-%d"),
            "expiration_date": expiration_date.strftime("%Y-%m-%d"),
            "days_valid": expiration_days,
            "max_activations": max_activations,
            "features": features,
            "machine_id": machine_id or "",
            "activation_key": activation_key,
            "license_type": license_type
        }
    
    @staticmethod
    def _generate_signature(license_data: dict) -> str:
        """Generate cryptographic signature for license data"""
        # Create string from key data
        machine_part = license_data.get("machine_id", "")
        data_string = (
            f"{license_data['license_id']}"
            f"{license_data['company_name']}"
            f"{license_data['expiration_date']}"
            f"{machine_part}"
            f"{LicenseGenerator.MASTER_SECRET}"
        )
        
        # Generate SHA256 hash
        signature = hashlib.sha256(data_string.encode()).hexdigest()
        return signature[:32]  # Use first 32 chars

    @staticmethod
    def _build_activation_key(machine_id: str, expiration_date: datetime, license_type: str) -> str:
        """Create activation key compatible with main application."""
        key_type = license_type[:3].upper()
        data = f"{machine_id}|{expiration_date.strftime('%Y-%m-%d')}|{key_type}"
        signature = hashlib.sha256((data + LICENSE_SALT.decode('latin-1')).encode()).hexdigest()
        return f"{machine_id}-{expiration_date.strftime('%Y%m%d')}-{key_type}-{signature[:8].upper()}"
    
    @staticmethod
    def _encode_license(license_data: dict) -> str:
        """Encode license data into a key string"""
        # Convert to JSON
        json_data = json.dumps(license_data, separators=(',', ':'))
        
        # Encode to base64
        encoded = base64.b64encode(json_data.encode()).decode()
        
        # Format as XXXX-XXXX-XXXX-XXXX
        formatted_key = '-'.join([encoded[i:i+4] for i in range(0, min(len(encoded), 16), 4)])
        
        return f"NARONG-{formatted_key}-{encoded[16:]}"
    
    @staticmethod
    def verify_license_key(license_key: str) -> tuple:
        """
        Verify a license key
        
        Returns:
            (is_valid, license_data or error_message)
        """
        try:
            # Remove NARONG- prefix and decode
            if not license_key.startswith("NARONG-"):
                return False, "Invalid license key format"
            
            # Extract encoded data
            key_parts = license_key[7:].split('-')
            encoded_data = ''.join(key_parts)
            
            # Decode from base64
            decoded = base64.b64decode(encoded_data).decode()
            license_data = json.loads(decoded)
            
            # Verify signature
            expected_signature = LicenseGenerator._generate_signature(license_data)
            if license_data.get("signature") != expected_signature:
                return False, "Invalid license signature"
            
            # Check expiration
            expiration_date = datetime.fromisoformat(license_data["expiration_date"])
            if datetime.now() > expiration_date:
                return False, f"License expired on {expiration_date.strftime('%Y-%m-%d')}"
            
            return True, license_data
            
        except Exception as e:
            return False, f"License verification failed: {str(e)}"


class LicenseGeneratorGUI(QtWidgets.QMainWindow):
    """GUI for license key generation"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔑 NARONG CCTV License Key Generator")
        self.setMinimumSize(700, 600)
        
        # Main app style matching
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f6f6f6;
                font-family: Arial;
                font-size: 12px;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ddd;
                padding: 6px;
                margin-top: 8px;
                background-color: #fff;
                border-radius: 4px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2c3e50;
                background-color: #f6f6f6;
            }
            QLineEdit, QComboBox, QSpinBox {
                padding: 6px 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #fff;
                font-size: 12px;
                min-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border: 2px solid #3498db;
            }
            QLineEdit:hover, QComboBox:hover, QSpinBox:hover {
                border: 1px solid #3498db;
            }
            QPushButton {
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            QTextEdit {
                border: 2px solid #dcdde1;
                border-radius: 6px;
                padding: 10px;
                background-color: #f8f9fa;
                font-family: 'Courier New';
                font-size: 10pt;
            }
        """)
        
        # Central widget
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Main app style header
        header_layout = QtWidgets.QVBoxLayout()
        header_layout.setSpacing(10)
        header_layout.setContentsMargins(0, 10, 0, 15)
        
        title_label = QtWidgets.QLabel("🔑 NARONG CCTV License Generator")
        title_label.setStyleSheet("""
            font-size: 18pt; 
            font-weight: bold; 
            color: #2c3e50;
            padding: 10px 0;
        """)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        
        subtitle_label = QtWidgets.QLabel("Enhanced Edition v8.7 - Master Key Generation Tool")
        subtitle_label.setStyleSheet("""
            font-size: 11pt; 
            color: #34495e;
            padding-bottom: 5px;
        """)
        subtitle_label.setAlignment(QtCore.Qt.AlignCenter)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        
        layout.addLayout(header_layout)
        
        # Input form
        form_group = QtWidgets.QGroupBox("📋 Customer Information")
        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(15)
        
        self.company_input = QtWidgets.QLineEdit()
        self.company_input.setPlaceholderText("Enter customer company name...")
        self.company_input.setStyleSheet("padding: 8px; font-size: 10pt;")
        form_layout.addRow("Company Name:", self.company_input)
        
        # Customer Machine ID field
        self.machine_id_input = QtWidgets.QLineEdit()
        self.machine_id_input.setPlaceholderText("Paste customer's Machine ID here...")
        self.machine_id_input.setStyleSheet("padding: 8px; font-family: 'Courier New'; font-size: 9pt; background-color: #ecf0f1;")
        form_layout.addRow("Customer Machine ID:", self.machine_id_input)
        
        self.expiration_combo = QtWidgets.QComboBox()
        self.expiration_combo.addItems([
            "30 days (Trial)",
            "90 days (Quarterly)",
            "365 days (Annual) - Recommended",
            "730 days (2 Years)",
            "Custom days..."
        ])
        self.expiration_combo.setCurrentIndex(2)
        self.expiration_combo.currentIndexChanged.connect(self._on_expiration_changed)
        form_layout.addRow("License Period:", self.expiration_combo)
        
        self.custom_days_input = QtWidgets.QSpinBox()
        self.custom_days_input.setRange(1, 3650)
        self.custom_days_input.setValue(365)
        self.custom_days_input.setEnabled(False)
        form_layout.addRow("Custom Days:", self.custom_days_input)
        
        self.activations_input = QtWidgets.QSpinBox()
        self.activations_input.setRange(1, 10)
        self.activations_input.setValue(1)
        form_layout.addRow("Max Activations:", self.activations_input)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Generate button
        generate_btn = QtWidgets.QPushButton("🔨 Generate License Key")
        generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        generate_btn.clicked.connect(self._generate_license)
        layout.addWidget(generate_btn)
        
        # Output area
        output_group = QtWidgets.QGroupBox("✅ Generated License Information")
        output_layout = QtWidgets.QVBoxLayout()
        
        # Short license key display
        key_display_label = QtWidgets.QLabel("📋 Generated License Key:")
        key_display_label.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 11pt; margin-top: 10px;")
        output_layout.addWidget(key_display_label)
        
        self.key_display = QtWidgets.QLineEdit()
        self.key_display.setReadOnly(True)
        self.key_display.setPlaceholderText("Generated license key will appear here...")
        self.key_display.setStyleSheet("""
            QLineEdit {
                font-family: 'Courier New';
                font-size: 11pt;
                padding: 12px;
                border: 2px solid #27ae60;
                border-radius: 6px;
                background-color: #f8f9fa;
                color: #2c3e50;
                selection-background-color: #3498db;
            }
        """)
        self.key_display.setFixedHeight(45)
        output_layout.addWidget(self.key_display)
        
        self.output_text = QtWidgets.QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMinimumHeight(150)
        self.output_text.setStyleSheet("""
            QTextEdit {
                font-family: Arial;
                font-size: 10pt;
                background-color: #fff;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px;
            }
            QTextEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        output_layout.addWidget(self.output_text)
        
        # Action buttons
        button_layout = QtWidgets.QHBoxLayout()
        
        copy_btn = QtWidgets.QPushButton("📋 Copy Key")
        copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        copy_btn.clicked.connect(self._copy_license_key)
        
        save_btn = QtWidgets.QPushButton("💾 Save")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #16a085;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #138d75;
            }
            QPushButton:pressed {
                background-color: #117864;
            }
        """)
        save_btn.clicked.connect(self._save_to_file)
        
        verify_btn = QtWidgets.QPushButton("🔍 Verify")
        verify_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
            QPushButton:pressed {
                background-color: #d35400;
            }
        """)
        verify_btn.clicked.connect(self._verify_key)
        
        button_layout.addWidget(copy_btn)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(verify_btn)
        
        output_layout.addLayout(button_layout)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        # Store generated license
        self.current_license = None
    
    def _on_expiration_changed(self, index):
        """Handle expiration combo change"""
        self.custom_days_input.setEnabled(index == 4)  # Custom option
    
    def _generate_license(self):
        """Generate license key"""
        company_name = self.company_input.text().strip()
        machine_id = self.machine_id_input.text().strip()
        
        if not company_name:
            QtWidgets.QMessageBox.warning(self, "Input Required", "Please enter a company name!")
            return
        
        if not machine_id:
            reply = QtWidgets.QMessageBox.question(
                self, 
                "Machine ID Missing",
                "⚠️ Customer Machine ID is not provided.\n\n"
                "The license key will still be generated, but you should record\n"
                "the customer's Machine ID for your records.\n\n"
                "Continue without Machine ID?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.No:
                return
        
        # Get expiration days
        expiration_index = self.expiration_combo.currentIndex()
        expiration_map = {0: 30, 1: 90, 2: 365, 3: 730}
        
        if expiration_index == 4:  # Custom
            expiration_days = self.custom_days_input.value()
        else:
            expiration_days = expiration_map[expiration_index]
        
        max_activations = self.activations_input.value()
        
        # Generate license
        license_info = LicenseGenerator.generate_license_key(
            company_name=company_name,
            expiration_days=expiration_days,
            max_activations=max_activations,
            features=["full_access"],
            machine_id=machine_id or None
        )
        
        self.current_license = license_info
        
        # Display key in the short display field
        activation_key = license_info['activation_key'] or license_info['license_key']
        self.key_display.setText(activation_key)
        
        # Display detailed information
        machine_id_section = (
            f"🖥️  Customer Machine ID: {machine_id}"
            if machine_id else
            "⚠️  Customer Machine ID: NOT PROVIDED"
        )
        activation_section = license_info['activation_key'] or 'Not generated - machine ID required'
        output = f"""╔═══════════════════════════════════════════════════════════╗
║           LICENSE KEY SUCCESSFULLY GENERATED              ║
╚═══════════════════════════════════════════════════════════╝

{machine_id_section}

🔐 ACTIVATION KEY (Use in Application):
{activation_section}

📋 LICENSE INFORMATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
License ID:       {license_info['license_id']}
Company:          {license_info['company_name']}
Issue Date:       {license_info['issue_date']}
Expiration:       {license_info['expiration_date']}
Valid Days:       {license_info['days_valid']} days
Max Activations:  {license_info['max_activations']}
Features:         {', '.join(license_info['features'])}
Stored License Key: {license_info['license_key']}

⚠️  IMPORTANT NOTES:
• Provide the ACTIVATION KEY above to the customer for in-app activation
• Keep the LICENSE KEY and metadata recorded securely for support
• License is machine-bound and cannot be transferred
• Backup this information in a secure location

✅ License generated and ready to use!"""
        
        self.output_text.setPlainText(output)
        
        # Show success message
        QtWidgets.QMessageBox.information(
            self,
            "Success",
            f"✅ License key generated successfully!\n\nValid for {expiration_days} days"
        )
    
    def _copy_license_key(self):
        """Copy license key to clipboard"""
        if not self.current_license:
            QtWidgets.QMessageBox.warning(self, "No License", "Please generate a license key first!")
            return
        
        clipboard = QtWidgets.QApplication.clipboard()
        key_to_copy = self.current_license.get('activation_key') or self.current_license['license_key']
        clipboard.setText(key_to_copy)
        
        # Visual feedback - temporarily change button text
        sender = self.sender()
        original_text = sender.text()
        sender.setText("✓ Copied!")
        sender.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
            }
        """)
        
        # Reset after 2 seconds
        QtCore.QTimer.singleShot(2000, lambda: (
            sender.setText(original_text),
            sender.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    font-weight: bold;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #21618c;
                }
            """)
        ))
    
    def _save_to_file(self):
        """Save license information to file"""
        if not self.current_license:
            QtWidgets.QMessageBox.warning(self, "No License", "Please generate a license key first!")
            return
        
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save License Information",
            f"license_{self.current_license['license_id']}_{self.current_license['company_name'].replace(' ', '_')}.json",
            "JSON Files (*.json)"
        )
        
        if filename:
            with open(filename, 'w') as f:
                json.dump(self.current_license, f, indent=2)
            
            QtWidgets.QMessageBox.information(
                self,
                "Saved",
                f"✅ License information saved to:\n{filename}"
            )
    
    def _verify_key(self):
        """Verify generated license key"""
        if not self.current_license:
            QtWidgets.QMessageBox.warning(self, "No License", "Please generate a license key first!")
            return
        
        is_valid, result = LicenseGenerator.verify_license_key(self.current_license['license_key'])
        
        if is_valid:
            days_remaining = (datetime.fromisoformat(result['expiration_date']) - datetime.now()).days
            QtWidgets.QMessageBox.information(
                self,
                "Verification Successful",
                f"✅ License key is VALID!\n\n"
                f"Company: {result['company_name']}\n"
                f"Days Remaining: {days_remaining}\n"
                f"License ID: {result['license_id']}"
            )
        else:
            QtWidgets.QMessageBox.critical(
                self,
                "Verification Failed",
                f"❌ License verification failed:\n\n{result}"
            )


def main_gui():
    """Launch GUI version"""
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set application icon
    app.setApplicationName("NARONG CCTV License Generator")
    
    window = LicenseGeneratorGUI()
    window.show()
    
    sys.exit(app.exec_())


def main():
    """Interactive license key generator"""
    print("=" * 60)
    print("NARONG CCTV LICENSE KEY GENERATOR")
    print("Master Key Generation Tool v8.7")
    print("=" * 60)
    print()
    
    # Get customer information
    company_name = input("Enter Company Name: ").strip()
    if not company_name:
        print("❌ Company name is required!")
        return
    
    # Get expiration period
    print("\nExpiration Period Options:")
    print("1. 30 days (Trial)")
    print("2. 90 days (Quarterly)")
    print("3. 365 days (Annual)")
    print("4. 730 days (2 Years)")
    print("5. Custom days")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    expiration_days_map = {
        "1": 30,
        "2": 90,
        "3": 365,
        "4": 730
    }
    
    if choice in expiration_days_map:
        expiration_days = expiration_days_map[choice]
    elif choice == "5":
        try:
            expiration_days = int(input("Enter custom days: "))
        except ValueError:
            print("❌ Invalid number!")
            return
    else:
        print("❌ Invalid choice!")
        return
    
    # Get activation limit
    try:
        max_activations = int(input("\nMaximum activations (1-10, default 1): ").strip() or "1")
        if max_activations < 1 or max_activations > 10:
            print("❌ Activations must be between 1 and 10!")
            return
    except ValueError:
        print("❌ Invalid number!")
        return
    
    # Generate license
    print("\n" + "=" * 60)
    print("⏳ Generating license key...")
    
    license_info = LicenseGenerator.generate_license_key(
        company_name=company_name,
        expiration_days=expiration_days,
        max_activations=max_activations,
        features=["full_access"]
    )
    
    print("✅ License key generated successfully!")
    print("=" * 60)
    print()
    print("LICENSE KEY INFORMATION:")
    print("-" * 60)
    print(f"License ID:      {license_info['license_id']}")
    print(f"Company:         {license_info['company_name']}")
    print(f"Issue Date:      {license_info['issue_date']}")
    print(f"Expiration:      {license_info['expiration_date']}")
    print(f"Valid Days:      {license_info['days_valid']}")
    print(f"Max Activations: {license_info['max_activations']}")
    print(f"Features:        {', '.join(license_info['features'])}")
    print("-" * 60)
    print()
    print("LICENSE KEY:")
    print("=" * 60)
    print(license_info['license_key'])
    print("=" * 60)
    print()
    
    # Verify the generated key
    print("🔍 Verifying license key...")
    is_valid, result = LicenseGenerator.verify_license_key(license_info['license_key'])
    
    if is_valid:
        print("✅ License key verification: PASSED")
        days_remaining = (datetime.fromisoformat(result['expiration_date']) - datetime.now()).days
        print(f"📅 Days remaining: {days_remaining}")
    else:
        print(f"❌ License key verification: FAILED - {result}")
    
    print()
    
    # Save to file
    save_choice = input("Save license information to file? (y/n): ").strip().lower()
    if save_choice == 'y':
        filename = f"license_{license_info['license_id']}_{company_name.replace(' ', '_')}.json"
        with open(filename, 'w') as f:
            json.dump(license_info, f, indent=2)
        print(f"✅ License information saved to: {filename}")
    
    print()
    print("=" * 60)
    print("⚠️  IMPORTANT: Keep the master secret secure!")
    print("⚠️  Share only the LICENSE KEY with customers")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    
    # Check if GUI mode requested or if running in GUI environment
    if len(sys.argv) > 1 and sys.argv[1] == '--gui':
        main_gui()
    elif len(sys.argv) == 1:
        # Default to GUI if no arguments
        try:
            main_gui()
        except Exception as e:
            print(f"GUI mode failed: {e}")
            print("\nFalling back to CLI mode...\n")
            try:
                main()
            except KeyboardInterrupt:
                print("\n\n❌ License generation cancelled by user")
            except Exception as e:
                print(f"\n\n❌ Error: {e}")
                import traceback
                traceback.print_exc()
    else:
        # CLI mode
        try:
            main()
        except KeyboardInterrupt:
            print("\n\n❌ License generation cancelled by user")
        except Exception as e:
            print(f"\n\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
