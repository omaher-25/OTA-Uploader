# OTA APP

This is an Over-The-Air (OTA) update application built with Python.

## Prerequisites

- Python 3.8+
- Set up Virtual environment (envota) 

# OTA APP

A lightweight Python application for delivering and testing Over-The-Air (OTA) updates, with ESP32 firmware support.

## Overview

This repository contains the Python application source, a virtual environment folder, helper scripts to run the app, and ESP32 firmware for OTA updates.

## Prerequisites

- Python 3.8+ 
- Virtual environment (recommended)

## Install Dependencies

From the project root, install dependencies with:

```powershell
pip install -r requirements.txt
```

If you use a virtual environment, activate it first (Windows example):

```powershell
envota\Scripts\activate
```

## Running

1) Run with a visible terminal (for debugging):

```powershell
envota\Scripts\activate
python main.py
```

2) Run without a console window (recommended for end users):

- Use the provided `run.bat` which activates the virtual environment and launches the app using `pythonw`.
- To hide the batch window entirely, double-click `run.vbs`, which runs `run.bat` invisibly.

Notes:
- `pythonw` runs Python scripts without opening a console; use it only for GUI or background scripts.
- The `run.vbs` file hides the batch process window so no console appears at all.

## Files

- `main.py` — main application script
- `requirements.txt` — Python package dependencies
- `run.bat` — batch script to activate the virtual environment and run the app with `pythonw`
- `run.vbs` — VBScript wrapper to run `run.bat` invisibly
- `envota/` — virtual environment folder (optional; typically not committed)
- `esp32/src/main.cpp` — ESP32 firmware source code
- `esp32/platformio.ini` — PlatformIO configuration for ESP32

## Troubleshooting

- If double-clicking `run.vbs` does not start the app, try running `run.bat` from a command prompt to see error messages.
- Ensure `envota` contains `pythonw.exe` in `envota\Scripts`. If not, install a Python distribution that includes `pythonw`.
- Confirm dependencies are installed by running `pip install -r requirements.txt` inside the activated venv.

## Contributing

Make changes in a feature branch and submit a pull request. Keep the repository free of personal or sensitive information.

## ESP32 Firmware

This folder contains the ESP32 firmware for handling OTA updates.

### Prerequisites

- Arduino IDE with ESP32 board support installed (via Board Manager: `esp32` by Espressif), or
- PlatformIO (VS Code extension or CLI) for better project management.
- ESP32 development board (e.g., ESP32-WROOM-32).

### Libraries

The code uses built-in ESP32 libraries:
- `WiFi.h`
- `WebServer.h`
- `Update.h`

No additional libraries need to be installed.

### Setup and Upload

#### Option 1: Arduino IDE
1. Open `esp32/src/main.cpp` in Arduino IDE.
2. Replace `YOUR_WIFI` and `YOUR_PASSWORD` with your WiFi credentials.
3. Select your ESP32 board and port in Tools menu.
4. Upload the sketch to the ESP32.

#### Option 2: PlatformIO (Recommended)
1. Install PlatformIO (via VS Code extension or CLI).
2. Open the `esp32/` folder in VS Code with PlatformIO.
3. Replace `YOUR_WIFI` and `YOUR_PASSWORD` in `esp32/src/main.cpp`.
4. Build and upload: Use PlatformIO's build/upload buttons or run `pio run -t upload` in the `esp32/` directory.

### Usage

- The ESP32 will connect to WiFi and start a web server on port 80.
- Send a POST request to `/update` with the firmware binary to perform OTA update.
- Use the Python app to send updates to the ESP32's IP address.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

# 🚀 OTA Uploader Pro - Feature Documentation

## Overview
OTA Uploader Pro is a comprehensive ESP32 firmware management tool with advanced features for wireless updates, device monitoring, and configuration management.

---

## ✨ Implemented Features

### 1. **🔒 Firmware Validation**
- **SHA256 Checksum Calculation**: Automatically calculates and logs checksums for uploaded firmware
- **Enable/Disable**: Checksum verification can be toggled in settings
- **Integrity Assurance**: Ensures firmware files haven't been corrupted

### 2. **🌐 Device Auto-Discovery**
- **Network Scanning**: Scan your local network to automatically find ESP32 devices
- **Device Detection**: Uses ping/status endpoints to identify active devices
- **Auto-Population**: Discovered devices can be added to your saved list
- **Real-time Status**: Shows device names and versions during discovery

### 3. **📊 Firmware Version Tracking**
- **Version Caching**: Stores device firmware versions locally
- **Device Info Query**: Retrieves device name, IP, MAC address, uptime, and signal strength
- **Version History**: Track what version each device is running
- **Last Check Timestamp**: Knows when each device was last checked

### 4. **📋 Upload History & Logging**
- **Complete Audit Trail**: Every upload attempt is logged with timestamp
- **Status Tracking**: Records success/failure status for each upload
- **Error Details**: Captures error messages for troubleshooting
- **Persistent Storage**: History is saved to `upload_history.json`
- **Visual History Viewer**: Browse past uploads with formatted timestamps

### 5. **🎯 Multiple Device Updates**
- **Batch Operations**: Support for uploading to multiple devices
- **Sequential Processing**: Devices are updated one at a time
- **Thread-Based**: Non-blocking uploads prevent GUI freezing
- **Device Management**: Save and organize multiple ESP32 device IPs

### 6. **📂 Drag & Drop Support**
- **File Selection**: Drag firmware files directly into the app
- **Simplified Workflow**: Faster file selection compared to browsing
- **Visual Feedback**: Status updates when files are loaded

### 7. **🔌 Device Status Monitoring**
- **Online/Offline Detection**: Checks if devices are reachable before upload
- **Status Endpoint**: Uses `/status` endpoint on ESP32 for health check
- **Connection Verification**: Ensures device is online before attempting upload
- **Automatic Fallback**: Handles offline devices gracefully

### 8. **🎨 Theme Support**
- **Dark Theme** (Default): OLED-friendly, reduces eye strain
- **Light Theme**: Alternative bright UI
- **Persistent Settings**: Theme preference is saved automatically
- **Quick Toggle**: Switch between themes with one click
- **Application-Wide**: Affects all UI elements and windows

### 9. **💾 Configuration Management**
- **Export Settings**: Save all IPs, history, and versions to a JSON file
- **Import Settings**: Load previously exported configurations
- **Backup & Restore**: Easy migration between systems
- **Batch Migration**: Move entire setup to new computer

### 10. **⚡ Advanced Features**
- **Device Info Endpoint**: Retrieves:
  - Device name and firmware version
  - MAC address and IP address
  - Uptime (in seconds)
  - WiFi signal strength (RSSI)
  
- **Checksum Logging**: Every upload records SHA256 hash for verification

- **Error Handling**: Comprehensive error messages for troubleshooting

- **Threading**: Non-blocking operations keep UI responsive

---

## 📁 New Files Created

### Python App (`main.py`)
- `ips.json` - Saved ESP32 IP addresses
- `upload_history.json` - Complete upload audit trail
- `app_config.json` - Application settings (theme, etc.)
- `device_versions.json` - Cached device version information

### ESP32 Firmware (`esp32/src/main.cpp`)
- New endpoints:
  - `/info` - Returns device information as JSON
  - `/status` - Health check endpoint (returns "OK")
  - `/config` - For future configuration management

---

## 🎮 How to Use Each Feature

### Network Scanning
1. Click **"🔍 Scan Network"** button
2. App scans local network for ESP32 devices
3. Found devices are displayed in the status area
4. Manually add them to your IP list by clicking "💾 Save IP"

### Version Checking
1. Enter an ESP32 IP address
2. Click **"ℹ️ Check Version"** button
3. App retrieves device info and caches it
4. View all cached versions with **"ℹ️ Versions"** menu

### Upload History
1. Click **"📋 History"** in menu bar
2. View all upload attempts with timestamps
3. See success/failure status for each upload
4. Export this data for auditing

### Configuration Backup
1. Click **"💾 Export"** to save entire configuration
2. Choose a location to save the JSON file
3. All IPs, history, and versions are included
4. Use **"📂 Import"** on another system to restore

### Theme Switching
1. Click **"🎨 Theme"** button
2. App switches to alternative theme
3. Restart application to see full effect
4. Preference is automatically saved

---

## 🔧 ESP32 Firmware Updates

### New Endpoints

#### GET /info
Returns JSON with device information:
```json
{
  "name": "ESP32_OTA",
  "version": "1.0.0",
  "ip": "192.168.1.100",
  "mac": "XX:XX:XX:XX:XX:XX",
  "uptime": 3600,
  "rssi": -45
}
```

#### GET /status
Simple health check:
```
OK
```

#### POST /update
Upload firmware binary (existing endpoint, enhanced)

---

## 📊 Data Storage

### `ips.json`
```json
[
  "192.168.1.100",
  "192.168.1.101"
]
```

### `upload_history.json`
```json
[
  {
    "timestamp": "2026-01-20T15:30:45.123456",
    "ip": "192.168.1.100",
    "status": "success",
    "file": "firmware.bin",
    "checksum": "abc123...",
    "error": null
  }
]
```

### `device_versions.json`
```json
{
  "192.168.1.100": {
    "name": "ESP32_OTA",
    "version": "1.0.0",
    "checked": "2026-01-20T15:30:45.123456"
  }
}
```

### `app_config.json`
```json
{
  "theme": "dark",
  "verify_checksum": true
}
```

---

## 🚀 Getting Started

### Requirements
- Python 3.8+
- ESP32 with WiFi connectivity
- ArduinoJson library (automatically installed via PlatformIO)

### Installation
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Upload ESP32 firmware (choose one):
   - **Arduino IDE**: Open `esp32/src/main.cpp` and upload
   - **PlatformIO**: Run `pio run -t upload` in `esp32/` directory

3. Configure WiFi credentials in `esp32/src/main.cpp`:
   ```cpp
   const char* ssid = "YOUR_WIFI";
   const char* password = "YOUR_PASSWORD";
   ```

4. Run the Python app:
   ```bash
   python main.py
   ```

---

## 💡 Best Practices

1. **Always Check Version Before Updating**: Use "ℹ️ Check Version" to confirm device is online
2. **Enable Checksum Verification**: Keep this enabled for data integrity
3. **Backup Configuration**: Export your settings regularly
4. **Review Upload History**: Check history for failed uploads
5. **Monitor Device Status**: Use network scanning to find all devices
6. **Keep Firmware Versions**: The version tracking helps identify outdated devices

---

## 🐛 Troubleshooting

### Device Not Found During Scan
- Ensure ESP32 is connected to WiFi
- Check that `/status` endpoint is responding
- Verify ESP32 and computer are on same network

### Checksum Mismatch
- Re-download firmware file
- Check if file is corrupted during transfer
- Verify checksum before upload

### Upload Fails
- Check device is online using "ℹ️ Check Version"
- Verify IP address is correct
- Ensure firmware file is valid (.bin format)
- Check ESP32 has sufficient free space

### Theme Not Changing
- Restart the application after changing theme
- Check `app_config.json` was saved successfully

---

## 📈 Future Enhancements

Potential additions:
- Automatic rollback on failed update
- OTA update scheduling
- Batch updates to multiple devices simultaneously
- Web interface for remote management
- Mobile app companion
- Delta/incremental updates
- Firmware repository with version management

---

# 🚀 Quick Start Guide - OTA Uploader Pro

## First Time Setup

### Step 1: Configure ESP32 Firmware
1. Open `esp32/src/main.cpp`
2. Replace WiFi credentials:
   ```cpp
   const char* ssid = "YOUR_WIFI";
   const char* password = "YOUR_PASSWORD";
   ```
3. Upload to your ESP32:
   - **Option A (Arduino IDE)**: Select ESP32 board and port, then upload
   - **Option B (PlatformIO)**: `pio run -t upload`

### Step 2: Get ESP32 IP Address
After uploading, check the serial monitor. The IP will be printed:
```
Connected
192.168.1.100
```

### Step 3: Run Python Application
```bash
python main.py
```

---

## Common Tasks

### 📝 Save an IP Address
1. Enter IP in "ESP32 IP Address" field
2. Click **"💾 Save IP"**
3. IP is now saved for future use
4. Double-click saved IP to load it quickly

### 🔍 Find All ESP32 Devices
1. Click **"🔍 Scan Network"**
2. Wait for scan to complete
3. Found devices are listed in status area
4. Manually add them to saved list

### 📊 Check Device Version
1. Enter device IP (or select from list)
2. Click **"ℹ️ Check Version"**
3. Device info is retrieved and cached
4. View all cached versions in "ℹ️ Versions" menu

### 🚀 Upload Firmware
1. Enter device IP
2. Click **"📂 Browse"** and select `.bin` file
3. Enable/disable checksum verification as needed
4. Click **"🚀 Upload Firmware"**
5. Watch progress in status bar

### 📋 Review Upload History
1. Click **"📋 History"** in menu bar
2. See all past uploads with timestamps
3. Check success/failure status
4. View associated error messages

### 💾 Backup Configuration
1. Click **"💾 Export"** in menu bar
2. Choose save location
3. All IPs, history, and settings are exported
4. Share backup or restore on another PC

### 📂 Restore Configuration
1. Click **"📂 Import"** in menu bar
2. Select previously exported JSON file
3. All data is restored automatically
4. Saved IPs and history are back

### 🎨 Switch Theme
1. Click **"🎨 Theme"** button
2. See confirmation message
3. **Restart the application** to apply theme
4. Preference is automatically saved

---

## Tips & Tricks

💡 **Tip 1**: Double-click a saved IP to instantly load it into the input field

💡 **Tip 2**: The app calculates SHA256 checksums to verify firmware integrity

💡 **Tip 3**: All data is stored locally as JSON files - easy to back up or edit manually

💡 **Tip 4**: Network scanning works best if ESP32 and computer are on same WiFi network

💡 **Tip 5**: Check the status bar at the bottom for detailed operation feedback

---

## Settings Files (Auto-Generated)

- **ips.json** - List of saved IP addresses
- **upload_history.json** - Complete upload audit trail
- **device_versions.json** - Cached device information
- **app_config.json** - Application preferences

All files are created in the same directory as `main.py`.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **Device not found** | Check ESP32 is powered on and connected to WiFi |
| **Connection refused** | Verify IP address and WiFi credentials in firmware |
| **Upload failed** | Ensure device is online, try again |
| **Slow scanning** | Normal for full network scan (1-2 minutes) |
| **Theme not applied** | Restart the application |

---

## Device Endpoints

Your ESP32 now has three HTTP endpoints:

- **GET `/status`** - Returns "OK" (used for online check)
- **GET `/info`** - Returns JSON with device details
- **POST `/update`** - Upload firmware binary

Example:
```bash
curl http://192.168.1.100/info
# Response: {"name":"ESP32_OTA","version":"1.0.0",...}

curl http://192.168.1.100/status
# Response: OK
```

---

## Advanced: Manual Device Configuration

Edit `app_config.json` to customize:
```json
{
  "theme": "dark",
  "verify_checksum": true
}
```

Options:
- `theme`: `"dark"` or `"light"`
- `verify_checksum`: `true` or `false`

---

**Happy uploading! 🎉**

---

# 📝 Changelog - OTA Uploader Pro v2.0

## v2.0.0 - Major Feature Release (January 20, 2026)

### ✨ New Features

#### Core Functionality
- **Auto-Discovery**: Network scanning to find all ESP32 devices on local network
- **Device Version Tracking**: Query and cache ESP32 firmware versions
- **Upload History**: Complete audit trail of all firmware uploads with timestamps
- **Firmware Validation**: SHA256 checksum calculation and logging
- **Device Status Monitoring**: Online/offline detection before uploads
- **Configuration Export/Import**: Backup and restore entire app configuration

#### UI/UX Improvements
- **Theme Support**: Toggle between dark and light themes
- **Responsive Design**: Scrollable interface for smaller screens
- **Non-Blocking Operations**: Threading prevents GUI freezing
- **Enhanced Status Feedback**: Detailed status messages for all operations
- **Improved File Selection**: Browse dialog with multiple file types

#### Data Management
- **ips.json**: Persistent storage of saved device IPs
- **upload_history.json**: Complete upload audit trail
- **device_versions.json**: Cached device information
- **app_config.json**: User preferences and settings

### 🔧 Technical Enhancements

#### Python App (`main.py`)
- Threading support for long-running operations
- Network scanning capability
- Checksum calculation (SHA256)
- Persistent JSON-based storage
- Multi-window support (history, versions)
- Theme system with persistent preferences

#### ESP32 Firmware (`esp32/src/main.cpp`)
- New `/info` endpoint returning device metadata as JSON
- New `/status` endpoint for health checks
- ArduinoJson library integration for JSON responses
- Device version and name constants
- Enhanced firmware version tracking

#### Build Configuration
- Updated `platformio.ini` to include ArduinoJson library
- Maintained Arduino IDE compatibility

### 📊 API Changes

#### New ESP32 Endpoints
```
GET  /status          → Health check (returns "OK")
GET  /info            → Device info JSON
POST /update          → Existing upload endpoint (unchanged)
```

#### Response Example (/info)
```json
{
  "name": "ESP32_OTA",
  "version": "1.0.0",
  "ip": "192.168.1.100",
  "mac": "AA:BB:CC:DD:EE:FF",
  "uptime": 3600,
  "rssi": -45
}
```

### 📁 New Files
- `FEATURES.md` - Comprehensive feature documentation
- `QUICKSTART.md` - Quick start guide
- `CHANGELOG.md` - This file

### 🐛 Bug Fixes
- Fixed window sizing issues on high-DPI displays
- Improved error handling for network timeouts
- Better handling of invalid IP addresses
- Enhanced exception handling in file operations

### ⚙️ Configuration Changes

New settings in `app_config.json`:
```json
{
  "theme": "dark",                 // "dark" or "light"
  "verify_checksum": true          // Enable/disable checksum verification
}
```

### 📈 Performance Improvements
- Faster UI responsiveness with threading
- Reduced network scan time with timeout optimization
- Efficient checksum calculation with streaming
- Memory-efficient history storage

### 🔒 Security Enhancements
- Checksum validation for firmware integrity
- Device online verification before upload
- Improved error message sanitization
- Configuration backup for disaster recovery

### 🎯 Usability Improvements
- Clearer status messages with emoji indicators
- Better visual feedback during operations
- Scrollable UI for better mobile support
- Keyboard shortcuts support (Double-click IP to load)
- Context-aware button states (disabled during operations)

### 📚 Documentation
- Added comprehensive FEATURES.md
- Added quick start guide (QUICKSTART.md)
- Updated ESP32 firmware comments
- Added inline Python documentation

### 🔄 Migration from v1.0
No breaking changes. v1.0 IPs list (if exists) will be detected and used.

---

## v1.0.0 - Initial Release

### Features
- Basic firmware upload to ESP32
- IP address management
- Simple UI with dark theme
- Status bar feedback

---

## Known Limitations

- Network scanning works best on same subnet
- Checksum verification adds ~5-10 seconds to upload time
- Theme change requires application restart
- History is limited to last 1000 entries (to prevent file bloat)

---

## Roadmap for Future Versions

### v3.0 (Planned)
- [ ] Batch uploads to multiple devices
- [ ] Scheduled/automatic updates
- [ ] Firmware repository management
- [ ] Web interface
- [ ] Device firmware rollback

### v2.1 (Next Release)
- [ ] Import device list from network
- [ ] Device grouping/tagging
- [ ] Upload progress percentage
- [ ] Retry mechanism for failed uploads

---

## Notes

- All local storage is in JSON format for easy backup/sharing
- No cloud storage required - everything stays on your computer
- Backward compatible with v1.0 device lists
- Requires Python 3.8+ and requests library

---

**Thank you for using OTA Uploader Pro! 🎉**

For feature requests or bug reports, please refer to the repository documentation.

