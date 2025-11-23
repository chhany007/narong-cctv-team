"""
IVMS-Style NVR Control Module
Provides NVR configuration, data extraction, and camera management capabilities
Supports Hikvision NVRs and ISAPI-compatible devices
"""

import json
import os
import sys
import socket

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import keyring


# ==================== CONSTANTS ====================
CONFIG_FILE = "nvr_config.json"
CREDENTIALS_SERVICE = "NVR_Control"
DEFAULT_TIMEOUT = 5.0
SADP_PORT = 37020

# Hikvision SADP discovery packet
SADP_REQUEST = bytes.fromhex(
    "3c3f786d6c2076657273696f6e3d22312e302220656e636f64696e673d227574662d38223f3e"
    "3c50726f626520636c6173734e616d653d2248696b766973696f6e223e3c2f50726f62653e"
)

# Common NVR API endpoints by vendor/model
NVR_ENDPOINTS = {
    "hikvision_isapi": {
        "device_info": "/ISAPI/System/deviceInfo",
        "cameras": [
            "/ISAPI/ContentMgmt/InputProxy/channels",
            "/ISAPI/System/Video/inputs/channels",
            "/ISAPI/ContentMgmt/RemoteDevice",
        ],
        "status": "/ISAPI/System/status",
        "channels": "/ISAPI/Streaming/channels",
    },
    "generic_api": {
        "cameras": ["/api/v1/devices", "/api/v2/devices"],
        "info": ["/api/v1/system/info", "/api/v2/system/info"],
    },
}


# ==================== CONFIGURATION MANAGEMENT ====================
class NVRConfig:
    """Manage NVR configuration including credentials and network settings"""

    def __init__(self, config_path: str = CONFIG_FILE):
        self.config_path = config_path
        self.nvrs = []
        self.load_config()

    def load_config(self):
        """Load NVR configuration from JSON file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.nvrs = data.get("nvrs", [])
                    print(f"✓ Loaded {len(self.nvrs)} NVR configurations")
            except Exception as e:
                print(f"✗ Error loading config: {e}")
                self.nvrs = []
        else:
            print(f"⚠ Config file not found: {self.config_path}")
            self.nvrs = []

    def save_config(self):
        """Save NVR configuration to JSON file"""
        try:
            data = {"nvrs": self.nvrs, "last_updated": datetime.now().isoformat()}
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✓ Configuration saved to {self.config_path}")
            return True
        except Exception as e:
            print(f"✗ Error saving config: {e}")
            return False

    def add_nvr(
        self,
        name: str,
        ip: str,
        username: str,
        password: str,
        model: str = "",
        port: int = 80,
        protocol: str = "http",
    ) -> bool:
        """Add a new NVR to configuration"""
        # Check if NVR already exists
        for nvr in self.nvrs:
            if nvr.get("name") == name or nvr.get("ip") == ip:
                print(f"✗ NVR already exists: {name} ({ip})")
                return False

        nvr_config = {
            "name": name,
            "ip": ip,
            "username": username,
            "port": port,
            "protocol": protocol,
            "model": model,
            "added": datetime.now().isoformat(),
        }

        self.nvrs.append(nvr_config)

        # Store password securely
        self.set_password(name, password)

        return self.save_config()

    def remove_nvr(self, name: str) -> bool:
        """Remove NVR from configuration"""
        for i, nvr in enumerate(self.nvrs):
            if nvr.get("name") == name:
                self.nvrs.pop(i)
                self.delete_password(name)
                return self.save_config()
        print(f"✗ NVR not found: {name}")
        return False

    def get_nvr(self, name: str) -> Optional[Dict]:
        """Get NVR configuration by name"""
        for nvr in self.nvrs:
            if nvr.get("name") == name:
                return nvr.copy()
        return None

    def list_nvrs(self) -> List[Dict]:
        """Get list of all configured NVRs"""
        return [nvr.copy() for nvr in self.nvrs]

    def update_nvr(self, name: str, **kwargs) -> bool:
        """Update NVR configuration"""
        for nvr in self.nvrs:
            if nvr.get("name") == name:
                # Update password separately if provided
                if "password" in kwargs:
                    self.set_password(name, kwargs.pop("password"))

                nvr.update(kwargs)
                nvr["last_modified"] = datetime.now().isoformat()
                return self.save_config()
        print(f"✗ NVR not found: {name}")
        return False

    # Password management using keyring
    def set_password(self, nvr_name: str, password: str):
        """Store password securely using keyring"""
        try:
            keyring.set_password(CREDENTIALS_SERVICE, nvr_name, password)
        except Exception as e:
            print(f"⚠ Could not store password securely: {e}")

    def get_password(self, nvr_name: str) -> Optional[str]:
        """Retrieve password from keyring"""
        try:
            pwd = keyring.get_password(CREDENTIALS_SERVICE, nvr_name)
            if pwd:
                return pwd
        except Exception as e:
            print(f"⚠ Could not retrieve password: {e}")

        # Fallback: read from nvr_credentials.json if keyring is missing
        try:
            creds_path = os.path.join(os.path.dirname(__file__), "nvr_credentials.json")
            if os.path.exists(creds_path):
                with open(creds_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for entry in data.values():
                    if entry.get("name") == nvr_name:
                        pwd = entry.get("password")
                        if pwd:
                            print(f"⚠ Using fallback password file for {nvr_name}")
                            return pwd
        except Exception as e:
            print(f"⚠ Fallback credential read error: {e}")
        return None

    def delete_password(self, nvr_name: str):
        """Delete password from keyring"""
        try:
            keyring.delete_password(CREDENTIALS_SERVICE, nvr_name)
        except Exception:
            pass


# ==================== NVR CONTROL CLASS ====================
class NVRController:
    """Main NVR control class for camera management and data extraction"""

    def __init__(self, config: NVRConfig = None):
        self.config = config or NVRConfig()
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Accept": "application/json, text/xml, */*",
            }
        )

    # ==================== CONNECTION & AUTHENTICATION ====================
    def test_connection(
        self, nvr_name: str, timeout: float = DEFAULT_TIMEOUT
    ) -> Tuple[bool, str, Dict]:
        """Test NVR connection and authentication"""
        nvr = self.config.get_nvr(nvr_name)
        if not nvr:
            return False, f"NVR not found: {nvr_name}", {}

        password = self.config.get_password(nvr_name)
        if not password:
            return False, "Password not found in keyring", {}

        ip = nvr["ip"]
        username = nvr["username"]
        protocol = nvr.get("protocol", "http")
        port = nvr.get("port", 80)

        base_url = f"{protocol}://{ip}:{port}" if port != 80 else f"{protocol}://{ip}"

        print(f"Testing connection to {nvr_name} ({ip})...")

        # Try multiple authentication methods
        auth_methods = [
            ("Basic", HTTPBasicAuth(username, password)),
            ("Digest", HTTPDigestAuth(username, password)),
        ]

        # Test endpoints in order of preference
        test_endpoints = [
            "/ISAPI/System/deviceInfo",
            "/api/v1/system/info",
            "/api/v2/system/info",
        ]

        for auth_name, auth in auth_methods:
            for endpoint in test_endpoints:
                url = base_url + endpoint
                try:
                    resp = self.session.get(url, auth=auth, timeout=timeout)
                    if resp.status_code == 200:
                        info = self._parse_response(resp)
                        print(f"✓ Connected using {auth_name} auth on {endpoint}")
                        return True, f"Connected ({auth_name})", info
                    elif resp.status_code == 401:
                        continue  # Try next auth method
                except requests.exceptions.Timeout:
                    continue
                except requests.exceptions.ConnectionError:
                    break  # No point trying other endpoints if can't connect

        return False, "Authentication failed or NVR unreachable", {}

    def _parse_response(self, response: requests.Response) -> Dict:
        """Parse JSON or XML response"""
        try:
            return response.json()
        except:
            try:
                root = ET.fromstring(response.text)
                return self._xml_to_dict(root)
            except:
                return {"raw": response.text}

    def _xml_to_dict(self, element: ET.Element) -> Dict:
        """Convert XML element to dictionary"""
        result = {}
        if element.text and element.text.strip():
            result["_text"] = element.text.strip()

        for child in element:
            tag = child.tag.split("}")[-1]  # Remove namespace
            child_data = self._xml_to_dict(child)
            if tag in result:
                if not isinstance(result[tag], list):
                    result[tag] = [result[tag]]
                result[tag].append(child_data)
            else:
                result[tag] = child_data

        return result if result else (element.text or "")

    # ==================== CAMERA LISTING ====================
    def list_cameras(
        self, nvr_name: str, timeout: float = DEFAULT_TIMEOUT
    ) -> Tuple[bool, List[Dict], str]:
        """
        List all cameras from NVR
        Returns: (success, camera_list, error_msg)
        Camera format: [{"name": str, "ip": str, "status": str, "channel": int}, ...]
        """
        nvr = self.config.get_nvr(nvr_name)
        if not nvr:
            return False, [], f"NVR not found: {nvr_name}"

        password = self.config.get_password(nvr_name)
        if not password:
            return False, [], "Password not found in keyring"

        ip = nvr["ip"]
        username = nvr["username"]
        protocol = nvr.get("protocol", "http")
        port = nvr.get("port", 80)

        print(f"\nFetching cameras from {nvr_name} ({ip})...")
        print(f"Using {username}@{ip}:{port} ({protocol})")

        # Test basic connectivity first
        try:
            test_url = f"{protocol}://{ip}:{port}/ISAPI/System/deviceInfo"
            print(f"Testing connectivity to {test_url}...")
            resp = self.session.get(test_url, auth=HTTPBasicAuth(username, password), timeout=2.0)
            print(f"  Device reachable: HTTP {resp.status_code}")
            if resp.status_code == 401:
                # Try digest auth for 401 responses
                print("  Trying Digest authentication...")
                try:
                    resp_digest = self.session.get(test_url, auth=HTTPDigestAuth(username, password), timeout=2.0)
                    print(f"  Digest auth: HTTP {resp_digest.status_code}")
                    if resp_digest.status_code != 200:
                        print("  Warning: deviceInfo endpoint auth failed, will try camera endpoints anyway")
                except Exception as e:
                    print(f"  Warning: digest auth exception {e}; continuing to other endpoints")
        except requests.exceptions.Timeout:
            return False, [], f"Connection timeout - NVR not reachable at {ip}:{port}"
        except requests.exceptions.ConnectionError:
            return False, [], f"Connection refused - check IP address and port"
        except Exception as e:
            print(f"  Connectivity test error: {e}")

        # Try multiple methods to get camera list
        cameras = []

        # Method 1: ISAPI ContentMgmt (Hikvision) - Now tries Digest first, then Basic
        print("\n[Method 1] Trying ISAPI endpoints (Digest-first)...")
        cameras, method = self._fetch_isapi_cameras(ip, username, password, timeout)
        if cameras:
            print(f"✓ Found {len(cameras)} cameras using {method}")
            return True, cameras, ""

        # Method 2: Generic API endpoints
        print("\n[Method 2] Trying Generic API endpoints...")
        cameras, method = self._fetch_generic_api_cameras(
            ip, username, password, timeout
        )
        if cameras:
            print(f"✓ Found {len(cameras)} cameras using {method}")
            return True, cameras, ""

        # Method 3: ISAPI Video Inputs - Now tries Digest first, then Basic
        print("\n[Method 3] Trying Video Input channels (Digest-first)...")
        cameras, method = self._fetch_video_inputs(ip, username, password, timeout)
        if cameras:
            print(f"✓ Found {len(cameras)} cameras using {method}")
            return True, cameras, ""

        # Method 4: Legacy fallback removed (redundant since Method 1 & 3 now try Digest)

        error_msg = (
            f"Could not retrieve camera list from NVR.\n\n"
            f"Troubleshooting:\n"
            f"1. Verify NVR IP: {ip}\n"
            f"2. Check credentials: {username}\n"
            f"3. Ensure NVR API is enabled\n"
            f"4. Check NVR model: {nvr.get('model', 'Unknown')}\n"
            f"5. Try accessing http://{ip} in browser\n\n"
            f"The NVR may use a non-standard API or require special configuration."
        )
        return False, [], error_msg

    def _fetch_isapi_cameras(
        self, ip: str, user: str, pwd: str, timeout: float
    ) -> Tuple[List[Dict], str]:
        """Fetch cameras using Hikvision ISAPI with Digest-first auth (matches main app)"""
        endpoints = [
            "/ISAPI/ContentMgmt/InputProxy/channels",
            "/ISAPI/ContentMgmt/RemoteDevice",
            "/ISAPI/System/Video/inputs/channels",
        ]

        # Try both authentication methods for each endpoint (Digest first, like main app)
        auth_methods = [
            ("Digest", HTTPDigestAuth(user, pwd)),
            ("Basic", HTTPBasicAuth(user, pwd))
        ]

        errors = []
        for endpoint in endpoints:
            url = f"http://{ip}{endpoint}"
            
            for auth_name, auth in auth_methods:
                try:
                    resp = self.session.get(url, auth=auth, timeout=timeout)
                    print(f"  Trying {endpoint} ({auth_name}): {resp.status_code}")
                    if resp.status_code == 200:
                        cameras = self._parse_isapi_cameras(resp.text)
                        if cameras:
                            return cameras, f"ISAPI {endpoint} ({auth_name})"
                    elif resp.status_code == 401:
                        errors.append(f"{endpoint} ({auth_name}): Authentication failed")
                        continue  # Try next auth method
                    else:
                        errors.append(f"{endpoint} ({auth_name}): HTTP {resp.status_code}")
                except Exception as e:
                    errors.append(f"{endpoint} ({auth_name}): {str(e)[:50]}")
                    continue

        if errors:
            print(f"  ISAPI errors: {'; '.join(errors[:3])}")
        return [], ""

    def _parse_isapi_cameras(self, xml_text: str) -> List[Dict]:
        """Parse ISAPI XML response for camera list"""
        cameras = []
        try:
            root = ET.fromstring(xml_text)
            # Handle XML namespace
            namespace = {'hikvision': 'http://www.hikvision.com/ver20/XMLSchema'}
            
            # Look for InputProxyChannel or RemoteDevice elements (with and without namespace)
            input_channels = (root.findall(".//hikvision:InputProxyChannel", namespace) + 
                            root.findall(".//InputProxyChannel"))
            remote_devices = (root.findall(".//hikvision:RemoteDevice", namespace) + 
                            root.findall(".//RemoteDevice"))

            for channel in input_channels + remote_devices:
                cam = {}

                # Extract channel info using simpler approach
                cam_id = channel.find(".//{http://www.hikvision.com/ver20/XMLSchema}id")
                if cam_id is None:
                    cam_id = channel.find(".//id")
                cam["channel"] = int(cam_id.text) if cam_id is not None else 0

                cam_name = channel.find(".//{http://www.hikvision.com/ver20/XMLSchema}name")
                if cam_name is None:
                    cam_name = channel.find(".//name")
                cam["name"] = (
                    cam_name.text if cam_name is not None else f"Camera {cam['channel']}"
                )

                # Extract IP address from sourceInputPortDescriptor
                ip_elem = channel.find(".//{http://www.hikvision.com/ver20/XMLSchema}ipAddress")
                if ip_elem is None:
                    ip_elem = channel.find(".//ipAddress") 
                cam["ip"] = ip_elem.text if ip_elem is not None else ""

                # Extract status - check for devIndex (present only when camera is actually connected)
                devindex_elem = channel.find(".//{http://www.hikvision.com/ver20/XMLSchema}devIndex")
                if devindex_elem is None:
                    devindex_elem = channel.find(".//devIndex")
                
                # Camera is online only if it has devIndex (indicates actual device connected)
                cam["status"] = "online" if devindex_elem is not None and devindex_elem.text else "offline"

                # Extract model if available
                model_elem = channel.find(".//{http://www.hikvision.com/ver20/XMLSchema}model")
                if model_elem is None:
                    model_elem = channel.find(".//model")
                cam["model"] = model_elem.text if model_elem is not None else ""

                if cam.get("ip"):  # Only add if has IP
                    cameras.append(cam)

        except Exception as e:
            print(f"Error parsing ISAPI XML: {e}")
            import traceback
            traceback.print_exc()

        return cameras

    def _fetch_generic_api_cameras(
        self, ip: str, user: str, pwd: str, timeout: float
    ) -> Tuple[List[Dict], str]:
        """Fetch cameras using generic API endpoints"""
        endpoints = ["/api/v1/devices", "/api/v2/devices", "/cgi-bin/api/v1/devices"]

        errors = []
        for endpoint in endpoints:
            url = f"http://{ip}{endpoint}"
            try:
                resp = self.session.get(
                    url, auth=HTTPBasicAuth(user, pwd), timeout=timeout
                )
                print(f"  Trying {endpoint}: {resp.status_code}")
                if resp.status_code == 200:
                    data = resp.json()
                    cameras = self._parse_generic_cameras(data)
                    if cameras:
                        return cameras, f"Generic API {endpoint}"
                elif resp.status_code == 401:
                    errors.append(f"{endpoint}: Authentication failed")
                else:
                    errors.append(f"{endpoint}: HTTP {resp.status_code}")
            except Exception as e:
                errors.append(f"{endpoint}: {type(e).__name__}")
                continue

        if errors:
            print(f"  Generic API errors: {'; '.join(errors[:3])}")
        return [], ""

    def _parse_generic_cameras(self, data: Any) -> List[Dict]:
        """Parse generic API JSON response"""
        cameras = []

        devices = []
        if isinstance(data, dict):
            devices = data.get("devices", [])
        elif isinstance(data, list):
            devices = data

        for idx, dev in enumerate(devices):
            cam = {
                "channel": idx + 1,
                "name": dev.get("name")
                or dev.get("deviceName")
                or f"Camera {idx + 1}",
                "ip": dev.get("ip") or dev.get("ipAddress") or dev.get("address") or "",
                "status": dev.get("status") or dev.get("state") or "unknown",
                "model": dev.get("model") or dev.get("deviceModel") or "",
            }

            if cam["ip"]:
                cameras.append(cam)

        return cameras

    def _fetch_video_inputs(
        self, ip: str, user: str, pwd: str, timeout: float
    ) -> Tuple[List[Dict], str]:
        """Fetch cameras using video input channels with Digest-first auth"""
        endpoints = [
            "/ISAPI/System/Video/inputs/channels",
            "/api/v1/System/Video/inputs/channels",
            "/ISAPI/Streaming/channels",
        ]

        # Try both authentication methods (Digest first, like main app)
        auth_methods = [
            ("Digest", HTTPDigestAuth(user, pwd)),
            ("Basic", HTTPBasicAuth(user, pwd))
        ]

        for endpoint in endpoints:
            url = f"http://{ip}{endpoint}"
            for auth_name, auth in auth_methods:
                try:
                    resp = self.session.get(url, auth=auth, timeout=timeout)
                    print(f"  Trying {endpoint} ({auth_name}): {resp.status_code}")
                    if resp.status_code == 200:
                        cameras = self._parse_video_channels(resp)
                        if cameras:
                            return cameras, f"Video Inputs {endpoint} ({auth_name})"
                    elif resp.status_code == 401:
                        continue  # Try next auth method
                except Exception as e:
                    continue

        return [], ""

    def _fetch_with_digest_auth(
        self, ip: str, user: str, pwd: str, timeout: float
    ) -> Tuple[List[Dict], str]:
        """Fetch cameras using Digest authentication (fallback)"""
        from requests.auth import HTTPDigestAuth

        endpoints = [
            "/ISAPI/ContentMgmt/InputProxy/channels",
            "/ISAPI/System/Video/inputs/channels",
        ]

        for endpoint in endpoints:
            url = f"http://{ip}{endpoint}"
            try:
                resp = self.session.get(
                    url, auth=HTTPDigestAuth(user, pwd), timeout=timeout
                )
                print(f"  Trying {endpoint} (Digest): {resp.status_code}")
                if resp.status_code == 200:
                    # Save XML for debugging
                    with open("debug_cameras.xml", "w", encoding="utf-8") as f:
                        f.write(resp.text)
                    cameras = self._parse_isapi_cameras(resp.text)
                    if cameras:
                        return cameras, f"ISAPI {endpoint} (Digest Auth)"
            except Exception as e:
                continue

        return [], ""

    def _parse_video_channels(self, response: requests.Response) -> List[Dict]:
        """Parse video channel response (JSON or XML)"""
        cameras = []

        try:
            # Try JSON first
            data = response.json()
            channels = []
            if isinstance(data, dict):
                channels = data.get("channels", [])
            elif isinstance(data, list):
                channels = data

            for idx, ch in enumerate(channels):
                cam = {
                    "channel": idx + 1,
                    "name": ch.get("name")
                    or ch.get("channelName")
                    or f"Channel {idx + 1}",
                    "ip": ch.get("ip") or ch.get("ipAddress") or "",
                    "status": ch.get("status") or "unknown",
                    "model": "",
                }
                if cam["ip"]:
                    cameras.append(cam)

        except:
            # Try XML
            try:
                root = ET.fromstring(response.text)
                for idx, channel in enumerate(root.findall(".//VideoInputChannel")):
                    cam = {"channel": idx + 1, "name": f"Channel {idx + 1}", "ip": ""}

                    name_elem = channel.find(".//name")
                    if name_elem is not None:
                        cam["name"] = name_elem.text

                    cameras.append(cam)
            except:
                pass

        return cameras

    # ==================== DATA EXTRACTION ====================
    def get_nvr_info(self, nvr_name: str) -> Tuple[bool, Dict, str]:
        """Get detailed NVR system information"""
        nvr = self.config.get_nvr(nvr_name)
        if not nvr:
            return False, {}, f"NVR not found: {nvr_name}"

        password = self.config.get_password(nvr_name)
        if not password:
            return False, {}, "Password not found"

        ip = nvr["ip"]
        username = nvr["username"]

        # Try multiple info endpoints
        info_endpoints = [
            "/ISAPI/System/deviceInfo",
            "/api/v1/system/info",
            "/api/v2/system/info",
        ]

        for endpoint in info_endpoints:
            url = f"http://{ip}{endpoint}"
            try:
                resp = self.session.get(
                    url, auth=HTTPBasicAuth(username, password), timeout=5.0
                )
                if resp.status_code == 200:
                    info = self._parse_response(resp)
                    return True, info, ""
            except Exception:
                continue

        return False, {}, "Could not retrieve NVR info"

    def get_camera_status(
        self, nvr_name: str, camera_ip: str
    ) -> Tuple[bool, str, Dict]:
        """Check status of specific camera on NVR"""
        success, cameras, error = self.list_cameras(nvr_name)
        if not success:
            return False, error, {}

        for cam in cameras:
            if cam["ip"] == camera_ip:
                return True, cam["status"], cam

        return False, "Camera not found on NVR", {}

    def export_camera_list(
        self, nvr_name: str, output_file: str = None
    ) -> Tuple[bool, str]:
        """Export camera list to CSV file"""
        success, cameras, error = self.list_cameras(nvr_name)
        if not success:
            return False, error

        if not output_file:
            output_file = f"{nvr_name}_cameras_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                # Write header
                f.write("NVR,Channel,Name,IP,Status,Model\n")

                # Write camera data
                for cam in cameras:
                    f.write(
                        f'{nvr_name},{cam.get("channel", "")},{cam.get("name", "")},'
                        f'{cam.get("ip", "")},{cam.get("status", "")},{cam.get("model", "")}\n'
                    )

            print(f"✓ Exported {len(cameras)} cameras to {output_file}")
            return True, output_file

        except Exception as e:
            return False, f"Error exporting: {e}"

    # ==================== NETWORK DISCOVERY ====================
    def discover_nvrs(self, timeout: float = 3.0) -> List[Dict]:
        """Discover NVRs on network using SADP protocol"""
        print("Discovering NVRs on network (SADP)...")
        discovered = []

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.settimeout(timeout)

            # Broadcast SADP request
            sock.sendto(SADP_REQUEST, ("<broadcast>", SADP_PORT))

            start_time = datetime.now()
            while (datetime.now() - start_time).total_seconds() < timeout:
                try:
                    data, addr = sock.recvfrom(4096)
                    device_info = self._parse_sadp_response(data, addr[0])
                    if device_info and device_info not in discovered:
                        discovered.append(device_info)
                        print(f"  Found: {device_info['model']} at {device_info['ip']}")
                except socket.timeout:
                    break

            sock.close()

        except Exception as e:
            print(f"Discovery error: {e}")

        print(f"✓ Discovered {len(discovered)} devices")
        return discovered

    def _parse_sadp_response(self, data: bytes, ip: str) -> Optional[Dict]:
        """Parse SADP response packet"""
        try:
            xml_text = data.decode("utf-8", errors="ignore")
            root = ET.fromstring(xml_text)

            device = {
                "ip": ip,
                "type": root.find(".//DeviceType")
                or root.find(".//deviceType")
                or "Unknown",
                "model": root.find(".//DeviceModel")
                or root.find(".//model")
                or "Unknown",
                "serial": root.find(".//SerialNo") or root.find(".//serialNumber") or "",
                "mac": root.find(".//MAC") or root.find(".//macAddress") or "",
            }

            # Extract text from elements
            for key in device:
                if hasattr(device[key], "text"):
                    device[key] = device[key].text or ""

            return device

        except Exception:
            return None


# ==================== CLI INTERFACE ====================
def main():
    """Command-line interface for NVR control"""
    import argparse

    parser = argparse.ArgumentParser(description="NVR Control System (IVMS-Style)")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Config commands
    config_parser = subparsers.add_parser("config", help="Manage NVR configuration")
    config_parser.add_argument("action", choices=["add", "remove", "list", "update"])
    config_parser.add_argument("--name", help="NVR name")
    config_parser.add_argument("--ip", help="NVR IP address")
    config_parser.add_argument("--user", help="Username")
    config_parser.add_argument("--password", help="Password")
    config_parser.add_argument("--model", help="NVR model")
    config_parser.add_argument("--port", type=int, default=80, help="Port (default: 80)")

    # Camera commands
    camera_parser = subparsers.add_parser("cameras", help="List cameras from NVR")
    camera_parser.add_argument("nvr_name", help="NVR name")
    camera_parser.add_argument("--export", help="Export to CSV file")

    # Info command
    info_parser = subparsers.add_parser("info", help="Get NVR system information")
    info_parser.add_argument("nvr_name", help="NVR name")

    # Test command
    test_parser = subparsers.add_parser("test", help="Test NVR connection")
    test_parser.add_argument("nvr_name", help="NVR name")

    # Discover command
    subparsers.add_parser("discover", help="Discover NVRs on network")

    args = parser.parse_args()

    config = NVRConfig()
    controller = NVRController(config)

    # Execute command
    if args.command == "config":
        if args.action == "list":
            nvrs = config.list_nvrs()
            print(f"\n{'Name':<15} {'IP':<15} {'Model':<20} {'User':<15}")
            print("=" * 70)
            for nvr in nvrs:
                print(
                    f"{nvr['name']:<15} {nvr['ip']:<15} {nvr.get('model', 'N/A'):<20} {nvr['username']:<15}"
                )

        elif args.action == "add":
            if not all([args.name, args.ip, args.user, args.password]):
                print("✗ Missing required arguments: --name, --ip, --user, --password")
                return
            config.add_nvr(
                args.name,
                args.ip,
                args.user,
                args.password,
                args.model or "",
                args.port,
            )

        elif args.action == "remove":
            if not args.name:
                print("✗ Missing --name argument")
                return
            config.remove_nvr(args.name)

    elif args.command == "cameras":
        success, cameras, error = controller.list_cameras(args.nvr_name)
        if success:
            print(f"\n{'Ch':<4} {'Name':<30} {'IP':<15} {'Status':<10} {'Model':<20}")
            print("=" * 85)
            for cam in cameras:
                model_txt = cam.get('model') or 'N/A'
                status_txt = cam.get('status') or 'Unknown'
                name_txt = cam.get('name') or 'Unnamed'
                ip_txt = cam.get('ip') or 'N/A'
                channel_txt = cam.get('channel', 'N/A')
                print(
                    f"{channel_txt:<4} {name_txt:<30} {ip_txt:<15} "
                    f"{status_txt:<10} {model_txt:<20}"
                )

            if args.export:
                controller.export_camera_list(args.nvr_name, args.export)
        else:
            print(f"✗ Error: {error}")

    elif args.command == "info":
        success, info, error = controller.get_nvr_info(args.nvr_name)
        if success:
            print("\nNVR Information:")
            print(json.dumps(info, indent=2))
        else:
            print(f"✗ Error: {error}")

    elif args.command == "test":
        success, msg, info = controller.test_connection(args.nvr_name)
        if success:
            print(f"✓ Connection successful: {msg}")
            if info:
                print("\nDevice Info:")
                print(json.dumps(info, indent=2))
        else:
            print(f"✗ Connection failed: {msg}")

    elif args.command == "discover":
        devices = controller.discover_nvrs()
        if devices:
            print(f"\n{'IP':<15} {'Type':<20} {'Model':<25} {'Serial':<20}")
            print("=" * 85)
            for dev in devices:
                print(
                    f"{dev['ip']:<15} {dev['type']:<20} {dev['model']:<25} {dev['serial']:<20}"
                )

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
